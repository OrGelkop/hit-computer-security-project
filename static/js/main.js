$(document).ready(function(e) {
    $('#allGamesButton').click(function(e){
        e.preventDefault();
        $('.modal-title').text("List all games");
        var content = `
        Only subscribed users can list all games<br><br>
        <form id="allGamesForm" name="allGamesForm" method="POST" action="/all_games">
            <input required type="email" name="allgamesmail" style="width: 70%" id="allGamesMail" placeholder="Enter email address"><br><br>
            <input type="submit" value="List" style="padding: 0 10px 0 10px">
        </form>
        `;
        $('.modal-text').html(content);
        $('#myModal').modal('show');
    });

/*    $('#allGamesForm').submit(function(e){
        e.preventDefault();
        $.ajax({
            url:'/all_games',
            type:'post',
            data:$('#allGamesForm').serialize(),
            success:function(result){
                alert(result);
            }
        });
    });
*/
    $('#requestForm').submit(function(e){
        e.preventDefault();
        $('.modal-title').text("Game request");
        $('.modal-text').text("");
        $('#loading').show();
        $('#myModal').modal('show');
        $.ajax({
            url:'/request',
            type:'post',
            data:$('#requestForm').serialize(),
            success:function(result){
                $('#loading').hide();
                $('.modal-text').text(result);
            }
        });
    });

    $('#subscribeForm').submit(function(e){
        e.preventDefault();
        $('.modal-title').text("Subscribing request");
        $('.modal-text').text("");
        $('#loading').show();
        $('#myModal').modal('show');
        $.ajax({
            url:'/subscribe',
            type:'post',
            data:$('#subscribeForm').serialize(),
            success:function(result){
                setTimeout(function() {
                    $('#loading').hide();
                    $('.modal-text').text(result);
                }, 2000);
            }
        });
    });
});