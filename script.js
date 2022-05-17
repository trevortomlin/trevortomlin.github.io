const GITHUB_API_REPO_URL="https://api.github.com/users/trevortomlin/repos"

$(document).ready(function () {
    
	window.ondragstart = function() {return false}

	repos = $.getJSON(GITHUB_API_REPO_URL, function( data ) {

		$.each( data, function(id, obj) {
			makeRepoCards(obj);
		  });

	});

	$("#sideBarCollapse").click(function() {

		$('#sidebar').toggleClass('collapsed');

	});

    $("#sidebar ul li").click(function() {

    	$('#sidebar ul li').removeClass('active');
    	$(this).addClass('active');

    	$('#content section').addClass('hidden');

    	if ($(this).children().hasClass('about')) {
    		$('#content .about-section').removeClass('hidden');
    	}
    	else if ($(this).children().hasClass('education')) {
    		$('#content .education-section').removeClass('hidden');
    	}
    	else if ($(this).children().hasClass('skills')) {
    		$('#content .skills-section').removeClass('hidden');
    	}
    	else if ($(this).children().hasClass('projects')) {
    		$('#content .projects-section').removeClass('hidden');
    	}
		else if ($(this).children().hasClass('events')) {
    		$('#content .events-section').removeClass('hidden');
    	}
    	
	});

});

function makeRepoCards(json) {

	section = document.getElementById("projects-section-column");

	var card = document.createElement("div");

	card.className = "card"
	card.style = "width: 20rem; height: 10rem;"

	var body = document.createElement("div");

	body.className = "card-body"

	var title = document.createElement("h5");

	title.innerHTML = json["name"];
	title.className = "card-title";

	var text = document.createElement("p");

	text.innerHTML = json["description"];
	text.className = "card-text";

	var link = document.createElement("a");

	link.innerHTML = "Link";
	link.href = json["html_url"];
	link.className = "card-link btn btn-primary";

	body.appendChild(title);
	body.appendChild(text);
	body.appendChild(link);

	card.appendChild(body);

	section.appendChild(card);

}