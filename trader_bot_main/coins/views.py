from django.shortcuts import render
from django.http import Http404

# Hardcoded coin data
coins = {
    "BTC": {
    "name": "Bitcoin",
    "description": "Bitcoin is the first decentralized digital currency, created in 2009 by an unknown person using the alias Satoshi Nakamoto. It allows peer-to-peer transactions on a secure and transparent blockchain, without the need for a central authority or intermediary. Bitcoin has become a revolutionary asset in the financial world, often compared to digital gold due to its limited supply and store of value characteristics.",
    "image": "btc.png"
    },
    "ETH": {
    "name": "Ethereum",
    "description": "Ethereum is a decentralized platform that enables developers to build and deploy smart contracts and decentralized applications (DApps). Created by Vitalik Buterin in 2015, Ethereum introduced the concept of a 'world computer' with its blockchain capable of running code in a trustless environment. Ether (ETH), the native cryptocurrency of the Ethereum network, powers transactions and operations on the platform, making it a critical part of the growing decentralized finance (DeFi) ecosystem.",
    "image": "eth.png"
    },
    "SOL": {
    "name": "Solana",
    "description": "Solana is a high-performance blockchain platform designed for decentralized applications and crypto-currencies. Launched in 2020 by Anatoly Yakovenko, Solana is known for its speed and low transaction costs, achieved through a unique consensus mechanism called Proof of History (PoH). Solana aims to scale throughput beyond what is typically achieved by popular blockchains while keeping costs low for users, making it a popular choice for DeFi and NFT projects.",
    "image": "sol.png"
    },
    "XRP": {
    "name": "Ripple (XRP)",
    "description": "Ripple is a real-time gross settlement system, currency exchange, and remittance network. Its cryptocurrency, XRP, is used to facilitate fast and cost-efficient cross-border transactions. Founded by Ripple Labs in 2012, XRP aims to enhance the global payments infrastructure by enabling instant and nearly free international transfers, often as a bridge currency between fiat currencies.",
    "image": "xrp.png"
    },
    "DOGE": {
    "name": "Dogecoin",
    "description": "Dogecoin started as a lighthearted 'meme coin' in 2013 but has grown into a significant player in the crypto world, largely due to its strong and vibrant community. Based on the popular 'Doge' meme, Dogecoin was created by Billy Markus and Jackson Palmer as a fun and friendly alternative to Bitcoin. Despite its origins, Dogecoin has been used for real-world transactions, tipping, and charitable donations, becoming known for its fast transactions and low fees.",
    "image": "doge.png"
    },
    "TON": {
    "name": "Toncoin (TON)",
    "description": "Toncoin is the native cryptocurrency of The Open Network (TON), a decentralized layer-1 blockchain initially developed by Telegram. TON is designed to handle millions of transactions per second, with ultra-fast processing speeds and low fees. It aims to be the backbone of a vast ecosystem of decentralized services, including DNS, payment solutions, and decentralized storage.",
    "image": "ton.png"
    },
    "TRX": {
    "name": "TRON (TRX)",
    "description": "TRON is a blockchain-based decentralized platform founded by Justin Sun in 2017. The TRON network aims to build a free, global digital content entertainment system with distributed storage technology. Its native cryptocurrency, TRX, is used to pay content creators directly, bypassing traditional gatekeepers like streaming services. TRON has grown rapidly and now supports decentralized applications, making it a competitor to Ethereum.",
    "image": "trx.png"
    },
    "ADA": {
    "name": "Cardano (ADA)",
    "description": "Cardano is a third-generation blockchain platform focused on sustainability, scalability, and transparency. Founded by Charles Hoskinson, one of the co-founders of Ethereum, Cardano is designed to be a more secure and balanced blockchain, leveraging a unique Proof of Stake (PoS) consensus mechanism called Ouroboros. The ADA cryptocurrency is used within the Cardano platform for staking and as a means of transfer.",
    "image": "ada.png"
    },
    "BNB": {
    "name": "Binance Coin (BNB)",
    "description": "Binance Coin (BNB) is the cryptocurrency issued by the Binance exchange, the world's largest crypto exchange by trading volume. Originally launched on the Ethereum blockchain as an ERC-20 token, BNB has since migrated to Binance’s proprietary blockchain, Binance Chain. BNB is used primarily to pay for transactions on the Binance exchange, but it also powers the Binance Smart Chain (BSC), a blockchain platform for developing decentralized applications.",
    "image": "bnb.png"
    },
    "USDC": {
    "name": "USD Coin (USDC)",
    "description": "USD Coin (USDC) is a fully collateralized stablecoin pegged to the US Dollar on a 1:1 basis. Issued by the Centre consortium, which includes Circle and Coinbase, USDC is built on the Ethereum blockchain and other chains for fast and transparent transactions. It is widely used in the DeFi space and as a reliable means of transferring and storing value without the volatility associated with other cryptocurrencies.",
    "image": "usdc.png"
    }
}

def coin_detail(request, symbol):
    symbol = symbol.upper()
    coin = coins.get(symbol)

    if not coin:
        raise Http404("Coin not found")

    context = {
        'symbol': symbol,
        'name': coin['name'],
        'description': coin['description'],
        'image': coin['image']
    }

    return render(request, 'coins/coin_detail.html', context)
