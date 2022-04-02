import sys

from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException

# Note that this is in Plancks.
# The Statemine ED is 1/10th that of the Kusama ED.
STATEMINE_EXISTENTIAL_DEPOSIT = 3333333
STATEMINE_NODE = "wss://statemine-rpc.polkadot.io"

# 10000000000 = 100 Billcoins (8 decimal places)

def transfer_ed_ksm(keypair, dest):
    try:

        call = substrate.compose_call(
            call_module='Balances',
            call_function='transfer',
            call_params={
                'dest': dest,
                'value': STATEMINE_EXISTENTIAL_DEPOSIT
            }
        )

    
        extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair, era={'period': 64})
    
        receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        print("Extrinsic '{}' sent and included in block '{}'".format(receipt.extrinsic_hash, receipt.block_hash))

    except SubstrateRequestException as e:
        print("Failed to send: {}".format(e))

def transfer_asset(keypair, asset_id, dest, amount):
    try:

        call = substrate.compose_call(
            call_module='Assets',
            call_function='transfer',
            call_params={
                'id': asset_id,
                'target': dest,
                'amount': amount
            }
        )

        extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair, era={'period': 64})

        receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        print("Extrinsic '{}' sent and included in block '{}'".format(receipt.extrinsic_hash, receipt.block_hash))

    except SubstrateRequestException as e:
        print("Failed to send: {}".format(e))

# This is ugly, and should probably be changed...
# Returns true if address is valid, false if not
def check_if_valid_address(addr):
    try:
        temp_call = substrate.compose_call(
            call_module='Balances',
            call_function='transfer',
            call_params={
                'dest': addr,
                'value': STATEMINE_EXISTENTIAL_DEPOSIT
            }
        )
        return True
    except:
        return False
    
        
def batch_send_eds(keypair, dest_list):

    try:

        calls = []
        for dest in dest_list:
            call = substrate.compose_call(
                call_module='Balances',
                call_function='transfer',
                call_params={
                    'dest': dest,
                    'value': STATEMINE_EXISTENTIAL_DEPOSIT
                }
            )
            calls.append(call)

        call = substrate.compose_call(
            call_module='Utility',
            call_function='batch',
            call_params={
                'calls': calls
            }
        )

    
        extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair, era={'period': 64})
        
        receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        print("Extrinsic '{}' sent and included in block '{}'".format(receipt.extrinsic_hash, receipt.block_hash))

    except SubstrateRequestException as e:
        print("Failed to send: {}".format(e))


    
def batch_send_assets(keypair, asset_id, dest_list, amount):
    
    try:

        calls = []
        for dest in dest_list:
            call = substrate.compose_call(
                call_module='Assets',
                call_function='transfer',
                call_params={
                    'id': asset_id,
                    'target': dest,
                    'amount': amount
                }
            )
            calls.append(call)

        call = substrate.compose_call(
            call_module='Utility',
            call_function='batch',
            call_params={
                'calls': calls
            }
        )

    
        extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair, era={'period': 64})
        
        receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        print("Extrinsic '{}' sent and included in block '{}'".format(receipt.extrinsic_hash, receipt.block_hash))

    except SubstrateRequestException as e:
        print("Failed to send: {}".format(e))



##########################################
# EXECUTION STARTS HERE
##########################################


# Check that a seed phrase is entered

if len(sys.argv) != 5:
    print("Arguments: asset_id amount_in_plancks filename seed_phrase_in_quotes")
    sys.exit("Could not read arguments")

print(sys.argv)
asset_id = sys.argv[1]
amount = sys.argv[2]
filename = sys.argv[3]
seed = sys.argv[4]

# Connect to node. By default this goes to Statemine, just change RPC endpoint to
# Statemint to use that instead.

print("Connecting to node...", end='')

substrate = SubstrateInterface(
    url=STATEMINE_NODE
)

print(" done!")

# Generate keypair

print("Generating keypair...", end='')

keypair = Keypair.create_from_mnemonic(seed)

print(" done!")

print("Reading in addresses...", end='')

text_file = open(filename, "r")
lines = text_file.readlines()
text_file.close()

print(" done!")

num_addresses = 0
dest_list = []

for line in lines:
    address = line.rstrip('\n')
    if len(address) < 2:
        continue
    if check_if_valid_address(address) == False:
        print(address + " is not a valid Statemine address, skipping.")
        continue
    
    num_addresses += 1
    print("Adding " + address + " to list")
    dest_list.append(address)

print("Sending EDs in batch...")
batch_send_eds(keypair, dest_list)
print("done!")

print("Sending assets in batch...")
batch_send_assets(keypair, asset_id, dest_list, amount)
print("done!")



print("Sent asset " + asset_id + " to " + str(num_addresses) + " accounts.")

