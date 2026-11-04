// SPDX-License-Identifier: MIT
pragma solidity 0.8.24;

/**
 * @title IPrivateEVMInstitutionalGate
 * @notice Interface for the Private EVM Institutional Gateway prototype.
 * @dev Models an institutional access and execution sequencer for private EVM subnets.
 */
interface IPrivateEVMInstitutionalGate {
    enum InstitutionStatus { Unregistered, Active, Suspended, Revoked }

    struct InstitutionalTransaction {
        address institution;
        address counterparty;
        uint256 amount;
        uint256 sequenceNonce;
        bytes32 assetIdentifier;
        bytes institutionalSignature;
    }

    struct ExecutionReceipt {
        bytes32 txHash;
        uint256 blockNumber;
        uint256 timestamp;
        uint256 gasConsumed;
        bool settled;
    }

    // Events
    event InstitutionRegistered(address indexed institution, bytes32 indexed legalEntityId, uint256 timestamp);
    event InstitutionStatusUpdated(address indexed institution, InstitutionStatus status, uint256 timestamp);
    event PrivateTransactionSequenced(
        bytes32 indexed txHash,
        address indexed institution,
        address indexed counterparty,
        uint256 amount,
        uint256 sequenceNonce
    );

    // Custom Errors
    error UnauthorizedInstitutionalCaller(address caller);
    error InvalidExecutionSequence(uint256 expectedNonce, uint256 providedNonce);
    error InstitutionalLaneSuspended(address institution);
    error InsufficientInstitutionalCollateral(uint256 available, uint256 requested);
    error ZeroAddressProhibited();
    error ZeroAmountProhibited();
    error InvalidInstitutionalSignature();
}
