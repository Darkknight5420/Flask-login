$(function () {
  $("form[name=signup_form], form[name=login_form]").on(
    "submit",
    function (e) {
      e.preventDefault();

      var $form = $(this);
      var $error = $form.find(".error");
      var $button = $form.find('[type="submit"]');
      var isSignup = $form.attr("name") === "signup_form";

      var $success = $form.find(".success-message");

      if (!$success.length) {
        $success = $("<p>")
          .addClass("success-message")
          .attr("role", "status")
          .css("color", "#167338")
          .hide();

        $form.append($success);
      }

      $error.text("").addClass("error--hidden");
      $success.text("").hide();
      $button.prop("disabled", true);

      $.ajax({
        url: isSignup ? "/user/signup" : "/user/login",
        type: "POST",
        data: $form.serialize(),
        dataType: "json",

        success: function (response) {
          if (isSignup) {
            // Stay on this page and show the signup message.
            $form[0].reset();
            $success.text(response.message).show();

            // Fill in the email on the login form.
            var $loginForm = $("form[name=login_form]");

            $loginForm.find('[name="email"]').val(response.email);
            $loginForm.find('[name="password"]').val("");
            $loginForm.find(".error")
              .text("")
              .addClass("error--hidden");
          } else {
            // Only successful login opens the dashboard.
            window.location.href = "/dashboard/";
          }
        },

        error: function (response) {
          var message =
            "Unable to complete the request. Check the VS Code terminal.";

          if (
            response.responseJSON &&
            response.responseJSON.error
          ) {
            message = response.responseJSON.error;
          }

          $error.text(message).removeClass("error--hidden");
        },

        complete: function () {
          $button.prop("disabled", false);
        }
      });
    }
  );
});