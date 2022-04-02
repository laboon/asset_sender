# asset_sender
Mass Send Statemine assets on Kusama

## Usage

This will send out the existential deposit and a selected amount of a Statemine asset to a list of addresses included in a file.

The file must include ONLY addresses, one per line.

Note: You will need to enter your seed phrase for the account at the command line. This is, of course, very insecure. I recommend using a pass-through account which only stores the amount of assets and KSM to be sent out.

### Command line arguments

1. asset_id - The Statemine asset ID you wish to send
2. amount_in_placks - The amount in Plancks you will send to each account. Note that different Statemine assets have different levels of precision!
3. filename - The filename to read, which should contain a list of Kusama addresses, one per line
4. seed_phrase_in_quotes - The seed phrase of the account from which a keypair will be generated and KSM/assets sent. Of course this account must already have some KSM and the asset you wish to send!

### Example

This example sends 100 Billcoins (asset ID 223) to the addresses found in filename.txt. Note that of course this is a dummy seed phrase; you will need to make your own Statemine account and fund it with KSM and the asset you wish to send.

```
python3 send.py 223 10000000000 filename.txt "end cry link reason crunch shine enroll supreme boost cluster fame devote"
```

## Usage on Statemint

This is meant for STATEMINE, not STATEMINT, assets.

To use on Statemint, change the STATEMINE_EXISTENTIAL_DEPOSIT and STATEMINE_NODE constants to the right Statemint values.

Ideally, this would support Statemine/Statemint selection from the command line. PRs accepted.

### Helpful Hint

Use `cat file.txt | grep -o "[CDEFGHIJKLMN][a-zA-Z0-9]\{45\}[a-zA-Z0-9]*" | uniq` to get a list of all Kusama addresses in file.txt

## Ideas for Improvement

1. Statemine/Statemint selector
2. Uses batch transactions (would also be much faster!)
3. Check that account exists before sending ED; don't sent it if it does

## Acknowledgements

Thanks to Polkascan for building the [Python Substrate Interface](https://github.com/polkascan/py-substrate-interface), on which this is built.
