

var timer = new Timer();
timer.start({countdown: true, startValues: {seconds: 5}});

$('#countdownExample .values').html(timer.getTimeValues().toString());

timer.addEventListener('secondsUpdated', function (e) {
    $('#countdownExample .values').html(timer.getTimeValues().toString());
});

timer.addEventListener('targetAchieved', function (e) {
    $('#countdownExample .values').html('Time is up');

$('#vote-button').hide()
});

