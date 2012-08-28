jQuery ->
    class KibaSession
        constructor: ->
            @first_name = ''
            @last_name = ''
            @avatar = ''

        @initWith: (resp) ->


    class GoogleSession extends KibaSession
        constructor: ->
            super()

        @initWith: (resp) ->
            name_parts = resp.displayName.split(' ')

            session = new GoogleSession()
            session.first_name = name_parts[0]
            session.last_name = name_parts[1]
            session.avatar = resp.image.url

            session


    class window.GoogleBackend
        scope: 'https://www.googleapis.com/auth/plus.me'

        @login: (@callback)->
            that = @
            gapi.auth.authorize({client_id: window.GOOGLE_CLIENT_ID, scope: @scope}, (authResult) ->
                if authResult && not authResult.error
                    gapi.client.load('plus', 'v1', ->
                        request = gapi.client.plus.people.get 'userId': 'me'
                        request.execute((resp) ->
                            callback(GoogleSession.initWith(resp))
                        )
                    )
            )


    class VkontakteSession extends KibaSession
        constructor: ->
            super()

        @initWith: (resp) ->
            session = new VkontakteSession()
            session.first_name = resp.user.first_name
            session.last_name = resp.user.last_name

            session


    class window.VkontakteBackend
        @login: (@callback)->
            VK.Auth.login((response) ->
                callback(VkontakteSession.initWith(response.session))
            )


    class FacebookSession extends KibaSession
        constructor: ->
            super()

        @initWith: (resp) ->
            session = new FacebookSession()
            session.first_name = resp.first_name
            session.last_name = resp.last_name


    class window.FacebookBackend
        @login: (@callback)->
            FB.login((response) ->
                FB.api('/me', (me)->
                    callback(FacebookSession.initWith(me))
                )
            )