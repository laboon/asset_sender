from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException


print("Connecting to node...", end='')

substrate = SubstrateInterface(
    url="wss://statemine-rpc.polkadot.io"
)

print(" done!")

print("Reading in addresses.txt...", end='')

text_file = open("addresses.txt", "r")
lines = text_file.readlines()
text_file.close()

print(" done!")

for line in lines:
        address = line.rstrip('\n')
        print(address)
