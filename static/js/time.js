

var timer = new Timer();
timer.start({countdown: true, startValues: {seconds: 60}});

$('#countdown-timer').html(timer.getTimeValues().toString());

timer.addEventListener('secondsUpdated', function (e) {
    $('#countdown-timer').html(timer.getTimeValues().toString());
});

timer.addEventListener('targetAchieved', function (e) {
    $('#countdown-timer').html('Time is up');

$('.vote-button').hide()
});

