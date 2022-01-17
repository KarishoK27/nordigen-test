var appAccounts = new Vue({
    el: '#accounts',
    delimiters: ['[[', ']]'],
    data: {
        accounts: []
    },
    methods: {
        getAccount: function (account) {
            let accounts = JSON.parse(document.getElementById('accounts_list').textContent)
            accounts.forEach(account => {
                $.ajax({
                    url: api_get_account_transactions_url,
                    type: "GET",
                    data: {
                        account: account.account
                    },
                    success: function (data, status, xhr) {
                        console.log(data)
                        appAccounts.accounts.push({
                            account: account.account,
                            transactions: data.transactions
                        })
                    }
                });
            });
            
        }
    },
    created() {
        this.getAccount()
    }
})