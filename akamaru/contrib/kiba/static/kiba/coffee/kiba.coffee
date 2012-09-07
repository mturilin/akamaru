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

            try_resolve_dfd = (r, key) ->
                if r.response and r.response.length
                    session[key] = r.response[0].name
                else
                    session[key] = ''

                if dfd_counter == 2
                    dfd.resolve(session)


            VK.Api.call('getCities', {cids: resp.city}, (r) ->
                dfd_counter += 1
                try_resolve_dfd(r, 'city')
            )

            VK.Api.call('getCountries', {cids: resp.country}, (r) ->
                dfd_counter += 1
                try_resolve_dfd(r, 'country')
            )

            dfd


        getFriends: (callback) ->
            VK.Api.call('friends.get', {fields: VkontakteSession.fields}, (r) ->
                callback(r.response)
            )


    class window.VkontakteBackend
        @fields: 'city,country,photo,photo_medium,photo_medium_rec,photo_big,photo_rec'

        @_me: (user_id, callback)->
            VK.Api.call('users.get', {uids: user_id, fields: VkontakteBackend.fields}, (r) ->
                VkontakteSession.initWith(r.response[0])
                    .done((session)->
                        callback(session)
                    )
            )

        @login: (callback, settings=2)->
            VK.Auth.getLoginStatus (lsResponse) ->
                if lsResponse.session
                    VkontakteBackend._me(lsResponse.session.mid, callback)
                else
                    VK.Auth.login((response) ->
                        VkontakteBackend._me(response.session.user.id, callback)
                    ,settings)


    class FacebookSession extends KibaSession
        constructor: ->
            super()

        @initWith: (me) ->
            session = new FacebookSession()
            session.first_name = me.first_name
            session.last_name = me.last_name
            session.id = me.id
            session.email = me.email

            if me.location
                location_parts = me.location.name.split(', ')
                if location_parts.length >= 2
                    session.city = location_parts[0]
                    session.country = location_parts[1]
                else
                    session.city = me.location
                    session.country = ''
            else
                session.city = ''
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
        @_me: (callback)->
            FB.api('/me', (me)->
                callback(FacebookSession.initWith(me))
            )

        @login: (callback, scope={scope: 'email,publish_stream'})->
            FB.getLoginStatus (lsResponse) ->
                if lsResponse.authResponse
                    FacebookBackend._me(callback)
                else
                    FB.login((response) ->
                        if response.authResponse
                            FacebookBackend._me(callback)
                        else
                            @
                    ,scope)



