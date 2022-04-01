import sys

from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException


def transfer_ksm(keypair, dest, amount):
    call = substrate.compose_call(
        call_module='Balances',
        call_function='transfer',
        call_params={
            'dest': 'JFArxqV6rqPSwBok3zQDnj5jL6vwsZQDwYXXqb1cFygnYVt',
            'value': 1 * 10**6
        }
    )

    extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair)

    try:
        receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        print("Extrinsic '{}' sent and included in block '{}'".format(receipt.extrinsic_hash, receipt.block_hash))

    except SubstrateRequestException as e:
        print("Failed to send: {}".format(e))

def transfer_asset(keypair, asset_id, dest, amount):
    print("tbd - transfer asset")

##########################################
# EXECUTION STARTS HERE
##########################################


# Check that a seed phrase is entered

if len(sys.argv) != 2:
    sys.exit("Enter seed phrase in quotes")

# Connect to node. By default this goes to Statemine, just change RPC endpoint to
# Statemint to use that instead

print("Connecting to node...", end='')

substrate = SubstrateInterface(
    url="wss://statemine-rpc.polkadot.io"
)

print(" done!")

# Generate keypair

print("Generating keypair...", end='')
    
seed = sys.argv[1]

keypair = Keypair.create_from_mnemonic(seed)

print(" done!")

transfer_ksm(keypair, "a", 1)
 
quit()

print("Reading in addresses.txt...", end='')

text_file = open("addresses.txt", "r")
lines = text_file.readlines()
text_file.close()

print(" done!")

for line in lines:
        address = line.rstrip('\n')
        print(address)


# # Set block_hash to None for chaintip
# block_hash = None

# # Retrieve extrinsics in block
# result = substrate.get_block(block_hash=block_hash)

# print(result)

# for extrinsic in result['extrinsics']:

#     if 'address' in extrinsic.value:
#         signed_by_address = extrinsic.value['address']
#     else:
#         signed_by_address = None

#     print('\nPallet: {}\nCall: {}\nSigned by: {}'.format(
#         extrinsic.value["call"]["call_module"],
#         extrinsic.value["call"]["call_function"],
#         signed_by_address
#     ))

#     # Loop through call params
#     for param in extrinsic.value["call"]['call_args']:

#         if param['type'] == 'Balance':
#             param['value'] = '{} {}'.format(param['value'] / 10 ** substrate.token_decimals, substrate.token_symbol)

#         print("Param '{}': {}".format(param['name'], param['value']))
