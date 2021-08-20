# Multi-Server-Blacklist
A discord bot that checks a database shared with multiple servers and punishes those on the database accordingly.

Our database is very simple, and the information stored is the following: (We have only 4 types of bans, software (hacks, clip review), racism, toxicity, and rulebreaks.
    When you are sending a request add two custom headers:
      username: ...
      password: ...
      
    Urls:
      /get_player <- GET
      body:
      {
        player_id: string or int
      }

    /get_players <- GET
    body:
    [
      {
        player_id: string or int
      },
      {
        player_id: string or int
      }
    ]

    /get_all <- GET
    body: Just send an empty body

    /set_player <- POST
    body:
    {
      player_id: string or int
      server_id: string or int
      assigner_id: ...
      type: bantype(listed above)
      reason: string
    }

    /set_players <- POST
    body:
    [
      {
        player_id: ... NOT NULL
        server_id: ... NOT NULL
        assigner_id: ...
        type: bantype(listed above)
        reason: string
      },
      {
        player_id: string or int
        server_id: string or int
        assigner_id: ...
        type: bantype(listed above)
        reason: string
      }
    ]

    /delete_player <- DELETE
    body:
    {
      player_id: string or int
    }

    /delete_players <- DELETE
    body:
    [
      {
        player_id: string or int
      },
      {
        player_id: string or int
      }
    ]

#What still needs to be added.

  -Add ban messages when logging and running checkbans()
  -Pages to embeds
  -Total stats
  -Help Page for commands.
