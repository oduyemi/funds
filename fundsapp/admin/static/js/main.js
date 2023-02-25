function smDevice(sm){
    if (sm.matches){
        document.body.style.backgroundColor="#0e34a0";
        document.getElementById('logo').src="images/logo/logo_white.png"
        document.getElementById("sm_msg").innerHTML=document.getElementById('_intro_msg').innerHTML
    }
}

var sm=window.matchMedia('(max-width:700px)');
    smDevice(sm);

$(document).ready(function(){
    $("#invest_group").hide();
    $(".ctabtn").hide();


    $("#invest_type").click(function(){
        var invest=$("#invest_type").children("option:selected").val();
        if(invest=="raise_fund"){
           $("#invest_type").hide();
           $("._dropdown").text("I am...")
           $("#invest_group").show();
           $("#ctabtn_ctd").show();
        }
    });

    $("#invest_type").click(function(){
        var invest=$("#invest_type").children("option:selected").val();
        if(invest=="invest"){
           $("#invest_type").hide();
           window.location.href="/invest"
        }
    });
    $("#ctabtn_ctd").click(function(){
        var investType=$("#invest_group").children("option:selected").val();
        if(investType=="ngo"){window.location.href="/ngo"}
        if(investType=="prestartup"){window.location.href="/prestartup"}
        if(investType=="startup"){window.location.href="/startup"}
        if(investType=="invest"){window.location.href="/invest"}
        if(investType==""){alert("Choose an option")}
    });

    $('.login').click(function(){
        window.location.href = '/login';
    });

    $('.signup').click(function(){
        window.location.href = '/signup';
    });




    $(".nav").click(function(){
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
  
    $(".nav2").click(function(){
      $(".mySidenav").css("width", "300px");
          $(".main").css("margin-left", "300px");
          $(".logo").css("visibility", "visible");
          $(".logo span").css("visibility", "visible");
          $(".icon-a").css("visibility", "visible");
          $(".icons").css("visibility", "visible");
          $(".nav").css("display", "block");
          $(".nav2").css("display", "none");
    });

    $('.b_dashboard').click(function(){
        window.location.href = '/dashboard';
    });

    $('.i_dashboard').click(function(){
        window.location.href = '/invest/dashboard';
    });

    $('.a_dashboard').click(function(){
        window.location.href = '/admin/dashboard';
    });

});
