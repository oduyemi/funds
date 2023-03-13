"use strict";

function smDevice(sm) {
  if (sm.matches) {
    document.body.style.backgroundColor = "#0e34a0";
    document.getElementById('logo').src = "images/logo/logo_white.png";
    document.getElementById("sm_msg").innerHTML = document.getElementById('_intro_msg').innerHTML;
  }
}

var sm = window.matchMedia('(max-width:700px)');
smDevice(sm);
$(document).ready(function () {
  $("#invest_group").hide();
  $(".ctabtn").hide();
  $("#invest_type").click(function () {
    var invest = $("#invest_type").children("option:selected").val();

    if (invest == "raise_fund") {
      $("#invest_type").hide();
      $("._dropdown").text("I am...");
      $("#invest_group").show();
      $("#ctabtn_ctd").show();
    }
  });
  $("#invest_type").click(function () {
    var invest = $("#invest_type").children("option:selected").val();

    if (invest == "invest") {
      $("#invest_type").hide();
      window.location.href = "/invest";
    }

    if (invest == "donate") {
      $("#invest_type").hide();
      window.location.href = "/donation";
    }
  });
  $("#ctabtn_ctd").click(function () {
    var investType = $("#invest_group").children("option:selected").val();

    if (investType == "ngo") {
      window.location.href = "/ngo";
    }

    if (investType == "prestartup") {
      window.location.href = "/prestartup";
    }

    if (investType == "startup") {
      window.location.href = "/startup";
    }

    if (investType == "invest") {
      window.location.href = "/invest";
    }

    if (investType == "donate") {
      window.location.href = "/donate";
    }

    if (investType == "") {
      alert("Choose an option");
    }
  });
  $('.login').click(function () {
    window.location.href = '/login';
  });
  $('.signup').click(function () {
    window.location.href = '/signup';
  });
  $('.signout').click(function () {
    window.location.href = '/signout';
  });
  $('.pro_pic').click(function () {
    window.location.href = '/profile/picture';
  });
  $(".nav").click(function () {
    $(".mySidenav").css("width", "70px");
    $(".main").css("margin-left", "70px");
    $(".logo").css("visibility", "hidden");
    $(".logo span").css("visibility", "visible");
    $(".logo span").css("margin-left", "-10px");
    $(".icon-a").css("visibility", "visible");
    $(".icons").css("visibility", "visible");
    $(".icons").css("margin-left", "-8px");
    $(".nav").css("display", "none");
    $(".nav2").css("display", "block");
  });
  $(".nav2").click(function () {
    $(".mySidenav").css("width", "300px");
    $(".main").css("margin-left", "300px");
    $(".logo").css("visibility", "visible");
    $(".logo span").css("visibility", "visible");
    $(".icon-a").css("visibility", "visible");
    $(".icons").css("visibility", "visible");
    $(".nav").css("display", "block");
    $(".nav2").css("display", "none");
  });
  $('.ngodashboard').click(function () {
    window.location.href = '/ngo/dashboard';
  });
  $('.ngolist').click(function () {
    window.location.href = '/ngolist/dashboard';
  });
  $('.ngoaccount').click(function () {
    window.location.href = '/ngoaccount/dashboard';
  });
  $('.ngocontact').click(function () {
    window.location.href = '/ngocontact/dashboard';
  });
  $('.ngopitch').click(function () {
    window.location.href = '/ngopitch/dashboard';
  });
  $('.ngoreviews').click(function () {
    window.location.href = '/ngoreviews/dashboard';
  });
  $('.startupdashboard').click(function () {
    window.location.href = '/startup/dashboard';
  });
  $('.startuplist').click(function () {
    window.location.href = '/startuplist/dashboard';
  });
  $('.startupaccount').click(function () {
    window.location.href = '/startupaccount/dashboard';
  });
  $('.startupcontact').click(function () {
    window.location.href = '/startupcontact/dashboard';
  });
  $('.startuppitch').click(function () {
    window.location.href = '/startuppitch/dashboard';
  });
  $('.startupreviews').click(function () {
    window.location.href = '/startupreviews/dashboard';
  });
  $('.prestartupdashboard').click(function () {
    window.location.href = '/prestartup/dashboard';
  });
  $('.prestartuplist').click(function () {
    window.location.href = '/prestartuplist/dashboard';
  });
  $('.prestartupaccount').click(function () {
    window.location.href = '/prestartupaccount/dashboard';
  });
  $('.prestartupcontact').click(function () {
    window.location.href = '/prestartupcontact/dashboard';
  });
  $('.prestartuppitch').click(function () {
    window.location.href = '/prestartuppitch/dashboard';
  });
  $('.prestartupreviews').click(function () {
    window.location.href = '/prestartupreviews/dashboard';
  });
  $('.funded').click(function () {
    window.location.href = '/funded';
  });
  $('.i_dashboard').click(function () {
    window.location.href = '/invest/dashboard';
  });
  $('.i_invest_dashboard').click(function () {
    window.location.href = '/invest/investment/dashboard';
  });
  $('.i_list_dashboard').click(function () {
    window.location.href = '/invest/list/dashboard';
  });
  $('.i_pitch_dashboard').click(function () {
    window.location.href = '/invest/pitch/dashboard';
  });
  $('.i_account_dashboard').click(function () {
    window.location.href = '/invest/account/dashboard';
  });
  $('.admindashboard').click(function () {
    window.location.href = '/admin/dashboard';
  });
  $(".base").click(function () {
    window.location.href = "/";
  });
  $('.logo').click(function () {
    window.location.href = '/';
  });
  $('.reg').click(function () {
    window.location.href = '/register';
  });
});
//# sourceMappingURL=main.dev.js.map
