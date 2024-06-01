const initProvider = () => {
    if ('panda' in window) {
        const provider = window.panda;
        if (provider?.isReady) {
            return provider;
        }
    }
    return null;
};

const loginWithPandaWallet = async () => {
    console.log("Attempting to log in with Panda Wallet...");
    await new Promise(resolve => setTimeout(resolve, 1000));
    const wallet = initProvider();
    if (!wallet) {
        console.error('Panda Wallet is not ready');
        document.getElementById('wallet-status').textContent = 'Panda Wallet is not ready. Please install and set up Panda Wallet.';
        window.open('https://chrome.google.com/webstore/detail/panda-wallet/mlbnicldl1pdjpfenfikcidjbokkgomo');
        return;
    }

    try {
        const accounts = await wallet.connect();
        if (accounts.length === 0) {
            console.log("No accounts found, ensure Panda Wallet is unlocked");
            alert('No accounts found. Please ensure your Panda Wallet is unlocked.');
            return;
        }
        const account = accounts[0];
        console.log('Logged in with Account:', account);
        const addresses = await wallet.getAddresses();
        console.log('Logged in with BSV Address:', addresses.bsvAddress);
        console.log('Logged in with Ordinals Address:', addresses.ordAddress);
        document.getElementById('walletAddress').value = addresses.ordAddress;

        const profile = await wallet.getSocialProfile();
        console.log('Profile:', profile);
        displayWalletInfo(profile.displayName, profile.avatar, addresses.ordAddress);
    } catch (error) {
        console.error('Error connecting to wallet:', error);
        document.getElementById('wallet-status').textContent = 'Failed to connect to wallet';
    }
};

const displayWalletInfo = (displayName, avatar, ordAddress) => {
    const profileContainer = document.getElementById('socialProfile');
    profileContainer.innerHTML = `
        <div class="profile">
            <img src="${avatar}" alt="Profile Picture" class="profile-pic">
            <p class="profile-name">${displayName}</p>
        </div>
    `;
    document.getElementById('wallet-status').textContent = `Logged in with Ordinals Address: ${ordAddress}`;
};

const enableAirdropButton = () => {
    const recipientGroups = document.querySelectorAll('.recipient-group');
    let valid = true;
    recipientGroups.forEach(group => {
        const wallet = group.querySelector('.recipientWallet').value.trim();
        const ordinal = group.querySelector('.ordinalId').value.trim();
        if (wallet === '' || ordinal === '') {
            valid = false;
        }
    });
    const airdropButton = document.getElementById('airdropButton');
    if (valid) {
        airdropButton.classList.add('glow-on-hover');
        airdropButton.disabled = false;
    } else {
        airdropButton.classList.remove('glow-on-hover');
        airdropButton.disabled = true;
    }
};

const performBatchTransfer = async () => {
    const wallet = initProvider();
    if (!wallet) {
        console.error('Panda Wallet is not ready');
        return;
    }

    const recipientGroups = document.querySelectorAll('.recipient-group');
    const transferParamsArray = [];

    recipientGroups.forEach(group => {
        const address = group.querySelector('.recipientWallet').value.trim();
        const ordinalId = group.querySelector('.ordinalId').value.trim();
        const transferParams = {
            address,
            origin: ordinalId,
            outpoint: ordinalId
        };
        transferParamsArray.push(transferParams);
    });

    try {
        for (const transferParams of transferParamsArray) {
            const txid = await wallet.transferOrdinal(transferParams);
            console.log('Transaction ID:', txid);
        }
        document.getElementById('result').innerText = 'Airdrop completed successfully.';
    } catch (err) {
        console.error('Error transferring ordinals:', err);
        document.getElementById('result').innerText = `Airdrop failed: ${err.message}`;
    }
};

document.addEventListener('DOMContentLoaded', () => {
    loginWithPandaWallet();
    document.getElementById('airdropButton').classList.remove('glow-on-hover');
    document.getElementById('airdropButton').disabled = true;

    document.getElementById('uploadJsonButton').addEventListener('click', function () {
        const fileInput = document.getElementById('jsonFile');
        const file = fileInput.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onload = function (event) {
                try {
                    const data = JSON.parse(event.target.result);
                    const recipientsContainer = document.getElementById('recipientsContainer');
                    recipientsContainer.innerHTML = ''; // Clear previous recipients

                    data.recipients.forEach(recipient => {
                        const newRecipientGroup = document.createElement('div');
                        newRecipientGroup.classList.add('form-group', 'recipient-group');
                        newRecipientGroup.innerHTML = `
                            <input type="text" class="recipientWallet" name="recipientWallet" value="${recipient.wallet_address}" required>
                            <input type="text" class="ordinalId" name="ordinalId" value="${recipient.ordinal_id}" required>
                            <button type="button" class="removeRecipientButton">Remove</button>
                        `;
                        recipientsContainer.appendChild(newRecipientGroup);

                        newRecipientGroup.querySelector('.removeRecipientButton').addEventListener('click', function () {
                            recipientsContainer.removeChild(newRecipientGroup);
                            enableAirdropButton();
                        });
                    });
                    enableAirdropButton();
                } catch (error) {
                    alert('Invalid JSON file.');
                }
            };
            reader.readAsText(file);
        } else {
            alert('Please select a JSON file.');
        }
    });

    document.getElementById('addRecipientButton').addEventListener('click', function () {
        const recipientsContainer = document.getElementById('recipientsContainer');
        const newRecipientGroup = document.createElement('div');
        newRecipientGroup.classList.add('form-group', 'recipient-group');
        newRecipientGroup.innerHTML = `
            <input type="text" class="recipientWallet" name="recipientWallet" placeholder="Recipient Wallet Address" required>
            <input type="text" class="ordinalId" name="ordinalId" placeholder="Ordinal ID" required>
            <button type="button" class="removeRecipientButton">Remove</button>
        `;
        recipientsContainer.appendChild(newRecipientGroup);

        newRecipientGroup.querySelector('.removeRecipientButton').addEventListener('click', function () {
            recipientsContainer.removeChild(newRecipientGroup);
            enableAirdropButton();
        });

        enableAirdropButton();
    });

    document.getElementById('airdropButton').addEventListener('click', async function (event) {
        event.preventDefault();
        performBatchTransfer();
    });

    document.getElementById('recipientsContainer').addEventListener('input', enableAirdropButton);
});
