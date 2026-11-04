// SPDX-License-Identifier: MIT
pragma solidity 0.8.24;

import { Test, console } from "forge-std/Test.sol";
import { PrivateEVMInstitutionalGate } from "../contracts/PrivateEVMInstitutionalGate.sol";
import { IPrivateEVMInstitutionalGate } from "../contracts/interfaces/IPrivateEVMInstitutionalGate.sol";

contract PrivateEVMInstitutionalGateTest is Test {
    PrivateEVMInstitutionalGate public gate;

    address public supervisor = address(0x1111);
    address public bankA = address(0xAAAA);
    address public bankB = address(0xBBBB);
    address public unauthorizedAttacker = address(0x9999);

    bytes32 public constant ASSET_USD_RESERVE = keccak256("WHOLESALE_CBDC_USD");
    bytes32 public constant LEI_BANK_A = keccak256("LEI_1234567890ABCDEFG");
    bytes32 public constant LEI_BANK_B = keccak256("LEI_0987654321GFEDCBA");

    event PrivateTransactionSequenced(
        bytes32 indexed txHash,
        address indexed institution,
        address indexed counterparty,
        uint256 amount,
        uint256 sequenceNonce
    );

    function setUp() public {
        vm.prank(supervisor);
        gate = new PrivateEVMInstitutionalGate(supervisor);

        // Register Bank A and Bank B
        vm.startPrank(supervisor);
        gate.registerInstitution(bankA, LEI_BANK_A);
        gate.registerInstitution(bankB, LEI_BANK_B);
        vm.stopPrank();

        // Bank A deposits 1,000,000 wholesale reserve tokens
        vm.prank(bankA);
        gate.depositCollateral(ASSET_USD_RESERVE, 1_000_000e18);
    }

    /// @notice Test 1: Happy Path - Valid private transaction executes and increments sequence
    function test_ValidInstitutionalPrivateExecution() public {
        IPrivateEVMInstitutionalGate.InstitutionalTransaction memory txn = IPrivateEVMInstitutionalGate.InstitutionalTransaction({
            institution: bankA,
            counterparty: bankB,
            amount: 250_000e18,
            sequenceNonce: 0,
            assetIdentifier: ASSET_USD_RESERVE,
            institutionalSignature: ""
        });

        vm.prank(bankA);
        bytes32 txHash = gate.executePrivateTransaction(txn);

        assertTrue(txHash != bytes32(0), "Transaction hash must not be zero");
        assertEq(gate.nextExpectedNonce(bankA), 1, "Nonce must increment to 1");
        assertEq(gate.collateralBalances(bankA, ASSET_USD_RESERVE), 750_000e18, "Bank A debited");
        assertEq(gate.collateralBalances(bankB, ASSET_USD_RESERVE), 250_000e18, "Bank B credited");
        assertEq(gate.totalTransactionsSequenced(), 1, "Total sequenced counter must be 1");
    }

    /// @notice Test 2: Counterfactual Test - Unauthorized attacker rejected at gate
    function test_RevertIf_UnauthorizedCaller() public {
        IPrivateEVMInstitutionalGate.InstitutionalTransaction memory txn = IPrivateEVMInstitutionalGate.InstitutionalTransaction({
            institution: unauthorizedAttacker,
            counterparty: bankB,
            amount: 50_000e18,
            sequenceNonce: 0,
            assetIdentifier: ASSET_USD_RESERVE,
            institutionalSignature: ""
        });

        vm.prank(unauthorizedAttacker);
        vm.expectRevert(
            abi.encodeWithSelector(
                IPrivateEVMInstitutionalGate.UnauthorizedInstitutionalCaller.selector,
                unauthorizedAttacker
            )
        );
        gate.executePrivateTransaction(txn);
    }

    /// @notice Test 3: Counterfactual Test - Out-of-order sequence nonce rejected
    function test_RevertIf_SequenceTampered() public {
        // Attempting to send nonce 5 when expected nonce is 0
        IPrivateEVMInstitutionalGate.InstitutionalTransaction memory txn = IPrivateEVMInstitutionalGate.InstitutionalTransaction({
            institution: bankA,
            counterparty: bankB,
            amount: 100_000e18,
            sequenceNonce: 5,
            assetIdentifier: ASSET_USD_RESERVE,
            institutionalSignature: ""
        });

        vm.prank(bankA);
        vm.expectRevert(
            abi.encodeWithSelector(
                IPrivateEVMInstitutionalGate.InvalidExecutionSequence.selector,
                0,
                5
            )
        );
        gate.executePrivateTransaction(txn);
    }

    /// @notice Test 4: Counterfactual Test - Replay of already executed nonce rejected
    function test_RevertIf_NonceReplayed() public {
        IPrivateEVMInstitutionalGate.InstitutionalTransaction memory txn = IPrivateEVMInstitutionalGate.InstitutionalTransaction({
            institution: bankA,
            counterparty: bankB,
            amount: 100_000e18,
            sequenceNonce: 0,
            assetIdentifier: ASSET_USD_RESERVE,
            institutionalSignature: ""
        });

        // 1st execution succeeds
        vm.prank(bankA);
        gate.executePrivateTransaction(txn);

        // 2nd execution with same nonce 0 must revert
        vm.prank(bankA);
        vm.expectRevert(
            abi.encodeWithSelector(
                IPrivateEVMInstitutionalGate.InvalidExecutionSequence.selector,
                1,
                0
            )
        );
        gate.executePrivateTransaction(txn);
    }

    /// @notice Test 5: Counterfactual Test - Overspend attempt exceeding collateral balance reverts
    function test_RevertIf_CollateralInsufficient() public {
        // Bank A only has 1,000,000e18, attempts to transfer 1,500,000e18
        IPrivateEVMInstitutionalGate.InstitutionalTransaction memory txn = IPrivateEVMInstitutionalGate.InstitutionalTransaction({
            institution: bankA,
            counterparty: bankB,
            amount: 1_500_000e18,
            sequenceNonce: 0,
            assetIdentifier: ASSET_USD_RESERVE,
            institutionalSignature: ""
        });

        vm.prank(bankA);
        vm.expectRevert(
            abi.encodeWithSelector(
                IPrivateEVMInstitutionalGate.InsufficientInstitutionalCollateral.selector,
                1_000_000e18,
                1_500_000e18
            )
        );
        gate.executePrivateTransaction(txn);
    }

    /// @notice Test 6: Counterfactual Test - Regulatory suspension instantly halts transaction flow
    function test_RevertIf_InstitutionalLaneSuspended() public {
        // Supervisor suspends Bank A
        vm.prank(supervisor);
        gate.updateInstitutionStatus(bankA, IPrivateEVMInstitutionalGate.InstitutionStatus.Suspended);

        IPrivateEVMInstitutionalGate.InstitutionalTransaction memory txn = IPrivateEVMInstitutionalGate.InstitutionalTransaction({
            institution: bankA,
            counterparty: bankB,
            amount: 10_000e18,
            sequenceNonce: 0,
            assetIdentifier: ASSET_USD_RESERVE,
            institutionalSignature: ""
        });

        vm.prank(bankA);
        vm.expectRevert(
            abi.encodeWithSelector(
                IPrivateEVMInstitutionalGate.InstitutionalLaneSuspended.selector,
                bankA
            )
        );
        gate.executePrivateTransaction(txn);
    }

    /// @notice Test 7: Deterministic Gas Profiling - Measures cold vs warm execution stability across 5 consecutive txs
    function test_DeterministicGasProfiling() public {
        uint256[5] memory gasUsed;

        for (uint256 i = 0; i < 5; i++) {
            IPrivateEVMInstitutionalGate.InstitutionalTransaction memory txn = IPrivateEVMInstitutionalGate.InstitutionalTransaction({
                institution: bankA,
                counterparty: bankB,
                amount: 10_000e18,
                sequenceNonce: i,
                assetIdentifier: ASSET_USD_RESERVE,
                institutionalSignature: ""
            });

            uint256 gasBefore = gasleft();
            vm.prank(bankA);
            gate.executePrivateTransaction(txn);
            gasUsed[i] = gasBefore - gasleft();

            console.log("Transaction", i + 1, "Gas Consumed:", gasUsed[i]);
            
            if (i == 0) {
                // Cold execution: initial balance slot initialization + receipt storage
                assertTrue(gasUsed[i] >= 210_000 && gasUsed[i] <= 240_000, "Initial execution gas bounded (210k-240k)");
            } else {
                // Warm execution: deterministic steady-state execution with receipt storage
                assertTrue(gasUsed[i] >= 165_000 && gasUsed[i] <= 185_000, "Steady-state gas bounded (165k-185k)");
            }
        }
    }
}
