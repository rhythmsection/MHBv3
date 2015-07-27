  $( "#about" ).onclick(function() {
    $('#main-div').html("");
    $( "#main-div" ).append( 
          "<p>MyHipsterBoyfriend is a music recognition system that enables the user to " +
          "record audio through their computer's microphone and compare it, using acoustic " +
          "fingerprinting and interval matching, to a self-seeded database of existing " +
          "acoustic fingerprints to find the best match for that song.</p>" +
          "<p>Please take a look at the documentation for further exploration of the "+
          "algorithm and subsequent functionality.</p>" );
  });


  $( "#instructions" ).click(function() {
    $('#main-div').html("");
    $( "#main-div" ).html( 
          "<ul>" +
          "<li>Fire up your Chrome browser (MHB does not work in Safari)</li>" +
          "<li>Click 'Allow' when the browser asks permission to use your microphone</li>" +
          "<li>Click the microphone button in the UI</li>" + 
          "<li>While the microphone is red (roughly 10 seconds), play a sample from one of "+
          "the listed tracks into your microphone</li>" +
          "</ul>" +
          "MyHipsterBoyfriend will attempt to match your clip with one of the songs in its "+
          "database. Have fun!");
  });


  $( "#database_list" ).click(function() {
    $('#main-div').html("");
    $( "#info_body" ).append( 
          "<table class='table'>" +
              "<tr>" +
                "<th>Song Title</th>" +
                "<th>Artist</th>" + 
              "</tr>" +
              "{% for song in songs_in_db %}" +
              "<tr>" +
                "<td>{{ song.title }}</td>" +
                "<td><i>{{ song.artist}}</i></td>" + 
              "</tr>" +
              "{% endfor %}" +
          "</table>" );
  });




            <table class="table">
                <tr>
                <th>Song Title</th>
                <th>Artist</th> 
              </tr>
              {% for song in songs_in_db %}
              <tr>
                <td>{{ song.title }}</td>
                <td><i>{{ song.artist}}</i></td> 
              </tr>
              {% endfor %}
            </table>