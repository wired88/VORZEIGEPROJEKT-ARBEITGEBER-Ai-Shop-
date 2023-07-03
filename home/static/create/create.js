
$(document).ready(function() {
    setInterval(function() {
        $.ajax({
            type: "GET",
            url: "/create/", // django urls wie {% home:create %} sind nicht zulässig
            success: function(response) {
                const temp_id = $('#display_tags');
                temp_id.empty();
                for (const key in response.pictures)
                {
                    const temp = '<div class="list-item">' + response.pictures[key].tag_field + '</div>';
                    temp_id.append(temp);
                }
            },
            error: function(response) {
                console.log('Wrong', response);
                alert('error!!!!!!!!!!!!!!!!!!');
            },
        });
    },2000); // nach wie viel ms die Seite aktualisiert werden soll
});
