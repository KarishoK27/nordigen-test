var appInstitutions = new Vue({
    el: '#institutions',
    delimiters: ['[[', ']]'],
    data: {
        institutions: []
    },
    methods: {
        getInstitutions: function () {
            let country = $("#country-select").val();

            $.ajax({
                url: api_get_institutions_url,
                type: "GET",
                data: {
                    country: country
                },
                success: function (data, status, xhr) {
                    console.log(data)
                    appInstitutions.institutions = data
                }
            });
        },
        selectBank: function (institution) {
            $.ajax({
                url: api_create_agreement_url,
                type: "POST",
                data: {
                    csrfmiddlewaretoken: csrf_token,
                    institution_id: institution.id
                },
                success: function (data, status, xhr) {
                    if (data.url) {
                        window.location.href = data.url;
                    }
                }
            });
        }
    },
    created() {
        this.getInstitutions()
    }
})