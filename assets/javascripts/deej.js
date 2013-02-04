var recstat = {
    IDLE: 0,
    PREPARING: 1,
    RECORDING: 2,
    LISTENING: 3,
    ENCODING: 4,
    UPLOADING: 5
};


var serstat = {
    NOTHING: 0,
    OK: 1,
    ERROR: -1,
    NOT_UNDERSTOOD: -2
};

$(document).ready(function(e) {
	Dajaxice.setup({'default_exception_callback': failed_status });

	/* block login */
	$("#user-list a").click(function(e) {
		e.preventDefault();
		$(this).addClass("active");
		$(this).parent().siblings().each(function(){
			$(this).hide();
		});
		$("#id_username").val($(this).data("username"));
		$("#login-form").show();
	});

	$("#login-cancel").click(function(e) {
		e.preventDefault();
		$("#login-form").hide();
		$("#id_password").val("");
		$("#user-list a.active").parent().siblings().each(function() {
			$(this).show();
			if($(this).hasClass("active")) $(this).removeClass("active");
		});
	});
	/* endblock login */

	/* block recording */
	$("#id_record").click(function(e) {
		e.preventDefault();
		$(this).prop("disabled", true);
		data = $('#record-form').serializeObject();
		Dajaxice.deej.recording.start(check_status, {'form':data});
	});
	$("#id_stop").click(function(e) {
		e.preventDefault();
		$(this).prop("disabled", true);
		Dajaxice.deej.recording.stop(check_status);
	});
	/* endblock recording */
});

var form_status = recstat.IDLE;

function check_status() {
	Dajaxice.deej.recording.status(write_status);
}

function recording_start(data) {
	$("#record-form").hide();
	$("#stop-form").show();
	$("#id_stop").prop("disabled", false);
	form_status = recstat.RECORDING;
	check_status();
}

function recording_stop(data) {
	$("#stop-form").hide();
	$("#record-form").show();
	$("#id_record").prop("disabled", false);
	$("#id_track").val("");
	form_status = recstat.IDLE;
	check_status();
}

function write_status(data) {
	var recording_status = "Idle";
	var recording_class = "";
	var uploading_status = "Idle";
	var uploading_class = "";

	if(data.recording_status == recstat.RECORDING) {
		recording_status = "Recording";
		recording_class = "success";

		if(form_status != recstat.RECORDING) {
			recording_start(false);
		}
	}
	else if (form_status != recstat.IDLE) {
		recording_stop(false);
	}

	if(data.uploading_status == recstat.UPLOADING) {
		uploading_status = "Uploading";
		uploading_class = "success";
	}

	$("#status").children().remove();
	$("#status").append(
		$("<p>", { 'text': "Record Status: "}).append(
			$("<span>", { 'text': recording_status, 'class': "label " + recording_class })));
	$("#status").append(
		$("<p>", { 'text': "Upload Status: "}).append(
			$("<span>", { 'text': uploading_status, 'class': "label " + uploading_class })));
}

function failed_status() {
	$("#status").children().remove();
	$("#status").append($("<span>", { 'text': "Error: Can't contact recorder", 'class': "label alert" }));
}