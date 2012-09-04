jQuery ->
    class KibaSession
        constructor: ->
            @first_name = ''
            @last_name = ''
            @avatar = ''
            @id = ''
            @city = ''
            @country = ''
            @access_token = ''

        @initWith: (resp) ->

        getFriends: (callback) ->
            []


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
        @scope: 'https://www.googleapis.com/auth/plus.me'

        @login: (callback)->
            that = @
            gapi.auth.authorize({client_id: window.GOOGLE_CLIENT_ID, scope: GoogleBackend.scope}, (authResult) ->
                if authResult && not authResult.error
                    gapi.client.load('plus', 'v1', ->
                        request = gapi.client.plus.people.get 'userId': 'me'
                        request.execute((resp) ->
                            callback(GoogleSession.initWith(resp))
                        )
                    )
            )


    class VkontakteSession extends KibaSession
        @fields: 'uid,first_name,last_name,nickname,sex,bdate,city,country,photo,photo_medium,photo_big'

        constructor: ->
            super()

        @initWith: (resp) ->
            session = new VkontakteSession()
            session.first_name = resp.first_name
            session.last_name = resp.last_name
            session.id = resp.uid

            dfd = $.Deferred()
            dfd_counter = 0

            VK.Api.call('getCities', {cids: resp.city}, (r) ->
                dfd_counter += 1
                session.city = r.response[0].name
                if dfd_counter == 2
                    dfd.resolve(session)
            )

            VK.Api.call('getCountries', {cids: resp.country}, (r) ->
                dfd_counter += 1
                session.country = r.response[0].name
                if dfd_counter == 2
                    dfd.resolve(session)
            )

            dfd


        getFriends: (callback) ->
            VK.Api.call('friends.get', {fields: VkontakteSession.fields}, (r) ->
                callback(r.response)
            )


    class window.VkontakteBackend
        @fields: 'city,country,photo,photo_medium,photo_medium_rec,photo_big,photo_rec'

        @login: (callback, settings=2)->
            VK.Auth.login((response) ->
                VK.Api.call('users.get', {uids: response.session.user.id, fields: VkontakteBackend.fields}, (r) ->
                    VkontakteSession.initWith(r.response[0])
                        .done((session)->
                            callback(session)
                        )
                )
            ,settings)


    class FacebookSession extends KibaSession
        constructor: ->
            super()

        @initWith: (response, me) ->
            session = new FacebookSession()
            session.first_name = me.first_name
            session.last_name = me.last_name
            session.id = me.id
            session.email = me.email

            session.access_token = response.authResponse.accessToken

            location_parts = me.location.name.split(', ')
            if location_parts.length >= 2
                session.city = location_parts[0]
                session.country = location_parts[1]
            else
                session.city = me.location
                session.country = ''

            session

        getFriends: (callback) ->
            FB.api('/me/friends', (friends)->
                friends_original = friends.data
                friends_mapped = $.map(friends_original, (elementOfArray, indexInArray) ->
                    name_parts = elementOfArray.split(' ')

                    first_name = ''
                    last_name = ''

                    if name_parts.length >= 2
                        first_name = name_parts[0]
                        last_name = name_parts[1]
                    else
                        first_name = elementOfArray.name

                    id: elementOfArray.id, name: elementOfArray.name, first_name: first_name, last_name: last_name
                )
                callback(friends_mapped)
            )


    class window.FacebookBackend
        @login: (callback, scope={scope: 'email,publish_stream'})->
            FB.login((response) ->
                if response.authResponse
                    FB.api('/me', (me)->
                        callback(FacebookSession.initWith(response, me))
                    )
            ,scope)