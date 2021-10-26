$(document).ready(function () {
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
    	
});
});