// SPDX-License-Identifier: MIT
pragma solidity 0.8.24;

import { IPrivateEVMInstitutionalGate } from "./interfaces/IPrivateEVMInstitutionalGate.sol";

/**
 * @title PrivateEVMInstitutionalGate
 * @notice Architectural prototype and invariant testbench for an Institutional Private EVM Gateway.
 * @dev Models private transaction ingress, deterministic local sequencer queue ordering,
 *      and strict KYC/status gates without public P2P mempool gossip.
 */
contract PrivateEVMInstitutionalGate is IPrivateEVMInstitutionalGate {
    address public immutable regulatorySupervisor;
    address public immutable gatewayOperator;

    // Institution registry: institution address => Status
    mapping(address => InstitutionStatus) public institutionStatus;
    // Institution legal identifier hash: institution address => LEI hash
    mapping(address => bytes32) public legalEntityIdentifiers;
    // Sequential execution nonce per institution: institution address => next expected nonce
    mapping(address => uint256) public nextExpectedNonce;
    // Internal ledger collateral: institution address => asset ID => balance
    mapping(address => mapping(bytes32 => uint256)) public collateralBalances;
    // Processed execution receipts: txHash => ExecutionReceipt
    mapping(bytes32 => ExecutionReceipt) public executionReceipts;

    // Total executed private transactions
    uint256 public totalTransactionsSequenced;

    modifier onlySupervisor() {
        if (msg.sender != regulatorySupervisor) {
            revert UnauthorizedInstitutionalCaller(msg.sender);
        }
        _;
    }

    modifier onlyActiveInstitution(address inst) {
        InstitutionStatus status = institutionStatus[inst];
        if (status == InstitutionStatus.Unregistered || status == InstitutionStatus.Revoked) {
            revert UnauthorizedInstitutionalCaller(inst);
        }
        if (status == InstitutionStatus.Suspended) {
            revert InstitutionalLaneSuspended(inst);
        }
        _;
    }

    constructor(address _supervisor) {
        if (_supervisor == address(0)) revert ZeroAddressProhibited();
        regulatorySupervisor = _supervisor;
        gatewayOperator = msg.sender;
    }

    /**
     * @notice Registers a new regulated institutional participant with its Legal Entity Identifier (LEI).
     */
    function registerInstitution(address institution, bytes32 legalEntityId) external onlySupervisor {
        if (institution == address(0)) revert ZeroAddressProhibited();
        institutionStatus[institution] = InstitutionStatus.Active;
        legalEntityIdentifiers[institution] = legalEntityId;
        emit InstitutionRegistered(institution, legalEntityId, block.timestamp);
        emit InstitutionStatusUpdated(institution, InstitutionStatus.Active, block.timestamp);
    }

    /**
     * @notice Updates the regulatory status of an institution (e.g. Active, Suspended, Revoked).
     */
    function updateInstitutionStatus(address institution, InstitutionStatus newStatus) external onlySupervisor {
        if (institution == address(0)) revert ZeroAddressProhibited();
        institutionStatus[institution] = newStatus;
        emit InstitutionStatusUpdated(institution, newStatus, block.timestamp);
    }

    /**
     * @notice Deposits collateral into the internal ledger for settlement.
     */
    function depositCollateral(bytes32 assetId, uint256 amount) external onlyActiveInstitution(msg.sender) {
        if (amount == 0) revert ZeroAmountProhibited();
        collateralBalances[msg.sender][assetId] += amount;
    }

    /**
     * @notice Executes a private institutional transaction within the private EVM execution queue.
     * @dev Enforces monotonic nonce sequence, active KYC status for both legs, and atomic balance debit/credit.
     */
    function executePrivateTransaction(
        InstitutionalTransaction calldata txn
    )
        external
        onlyActiveInstitution(txn.institution)
        onlyActiveInstitution(txn.counterparty)
        returns (bytes32 txHash)
    {
        // 1. Validate caller is either the institution itself or an authorized gateway operator
        if (msg.sender != txn.institution && msg.sender != gatewayOperator) {
            revert UnauthorizedInstitutionalCaller(msg.sender);
        }

        // 2. Enforce strict sequential nonce monotonicity (prevents out-of-order execution and replay)
        uint256 expected = nextExpectedNonce[txn.institution];
        if (txn.sequenceNonce != expected) {
            revert InvalidExecutionSequence(expected, txn.sequenceNonce);
        }
        nextExpectedNonce[txn.institution] = expected + 1;

        // 3. Validate amounts
        if (txn.amount == 0) revert ZeroAmountProhibited();

        // 4. Check available collateral
        uint256 currentBalance = collateralBalances[txn.institution][txn.assetIdentifier];
        if (currentBalance < txn.amount) {
            revert InsufficientInstitutionalCollateral(currentBalance, txn.amount);
        }

        // 5. Atomic settlement on internal private state
        unchecked {
            collateralBalances[txn.institution][txn.assetIdentifier] = currentBalance - txn.amount;
            collateralBalances[txn.counterparty][txn.assetIdentifier] += txn.amount;
        }

        // 6. Compute deterministic execution hash
        txHash = keccak256(
            abi.encode(
                txn.institution,
                txn.counterparty,
                txn.amount,
                txn.sequenceNonce,
                txn.assetIdentifier,
                block.chainid
            )
        );

        // 7. Store execution receipt
        executionReceipts[txHash] = ExecutionReceipt({
            txHash: txHash,
            blockNumber: block.number,
            timestamp: block.timestamp,
            gasConsumed: gasleft(),
            settled: true
        });

        totalTransactionsSequenced += 1;

        emit PrivateTransactionSequenced(
            txHash,
            txn.institution,
            txn.counterparty,
            txn.amount,
            txn.sequenceNonce
        );
    }
}
