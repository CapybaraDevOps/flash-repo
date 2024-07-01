$("form[name=signup_form]").submit(function(e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/signup",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            console.log(resp);
            window.location.href = "/user/dashboard/";
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

$("form[name=login_form]").submit(function(e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            console.log(resp);
            window.location.href = "/user/dashboard/";
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

$("form[name=update_data]").submit(function(e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/client/updata",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            console.log(resp);
            window.location.href = "/client/dashboard/";
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

$("form[name=service_update]").submit(function(e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    var url = $form.attr("action");
    $.ajax({
        url: url,
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            console.log(resp);
            window.location.href = "/user/dashboard/admin/";
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});


function addFn() {
    const divEle = document.getElementById("inputFields");
    divEle.innerHTML += `
<div>
    <form name="create_service_form">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required><br>
        <label for="serviceaddress">Address:</label>
        <input type="text" id="serviceaddress" name="serviceaddress" required><br>
        <label for="permission">Permission:</label>
        <input type="text" id="permission" name="permission" required><br>
        <label for="enabled">Enabled:</label>
        <input type="checkbox" id="enabled" name="enabled"><br>
        <button type="submit" class="btn btn--attention">Create</button>
    </form>
</div>
`;
}

$("form[name=create_service_form]").submit(function(e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/user/admin/service_create",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            console.log(resp);
            location.reload();
            // window.location.href = "/user/dashboard/";
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

function openForm() {
    document.getElementById("myForm").style.display = "block";
  }
  
function closeForm() {
    document.getElementById("myForm").style.display = "none";
  }


  $("form[name=roles_update]").submit(function(e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
    var url = $form.attr("action");
    $.ajax({
        url: url,
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            console.log(resp);
            window.location.href = "/user/dashboard/admin/";
        },
        error: function(resp) {
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});


