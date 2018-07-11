function navSearchHelper() {
}
navSearchHelper.prototype.submitSearch = function() {
    var query = this.getQueryString();
    var categories = this.getActiveCategories();
    var ageGroups = this.getActiveAgeGroups();
    var skills = this.getActiveSkills();
    var brands = this.getActiveBrands();
    var sorters = this.getSorters();
    //var urlParams = query;
    $("#_nav_search_form").append("<input type=\"hidden\" name="+ query[0].name+" value=\""+ query[0].value+"\">");
    var i;
    if(categories.length !== 0) {
        for(i = 0; i < categories.length; i++) {
            $("#_nav_search_form").append("<input type=\"hidden\" name="+ categories[i].name+" value=\""+ categories[i].value+"\">");
        }
        //urlParams += "&" + categories;
    }
    if(ageGroups.length !== 0) {
        for(i = 0; i < ageGroups.length; i++) {
            $("#_nav_search_form").append("<input type=\"hidden\" name="+ ageGroups[i].name+" value=\""+ ageGroups[i].value+"\">");
        }
        //urlParams += "&" + ageGroups;
    }
    if(skills.length !== 0) {
        for(i = 0; i < skills.length; i++) {
            $("#_nav_search_form").append("<input type=\"hidden\" name="+ skills[i].name+" value=\""+ skills[i].value+"\">");
        }
        //urlParams += "&" + ageGroups;
    }
    if(brands.length !== 0) {
        for(i = 0; i < brands.length; i++) {
            $("#_nav_search_form").append("<input type=\"hidden\" name="+ brands[i].name+" value=\""+ brands[i].value+"\">");
        }
        //urlParams += "&" + ageGroups;
    }

    if(sorters.length !== 0) {
        for(i = 0; i < sorters.length; i++) {
            $("#_nav_search_form").append("<input type=\"hidden\" name="+ sorters[i].name+" value=\""+ sorters[i].value+"\">");
        }
        
    } 
    //var searchUrl = "/toys/search?" + urlParams;
    //$("#_nav_search_form").attr("action", searchUrl);
    $("#_nav_search_form").submit();
}

navSearchHelper.prototype.getQueryString = function() {
    return $(".nav_search_form:visible").serializeArray();
}

navSearchHelper.prototype.getActiveCategories = function() {
    return $(".nav_category_form:visible").serializeArray();
}
navSearchHelper.prototype.getActiveAgeGroups = function() {
    return $(".nav_age_group_form:visible").serializeArray();
}

navSearchHelper.prototype.getActiveSkills = function() {
    return $(".nav_skills_form:visible").serializeArray();
}
navSearchHelper.prototype.getActiveBrands = function() {
    return $(".nav_brand_form:visible").serializeArray();
}
navSearchHelper.prototype.getSorters =function() {
    return $(".nav_search_sorter").serializeArray();
}

navSearchHelper.prototype.toggleFilterBar = function() {
    if($("#_nav_filter_side").hasClass("nav_sidenav_open")) {
        $("#_nav_filter_side").removeClass("nav_sidenav_open");
    }
    else {
        $("#_nav_filter_side").addClass("nav_sidenav_open");
    }
    if($(".nav_main_content").hasClass("nav_sidenav_open")) {
        $(".nav_main_content").removeClass("nav_sidenav_open");
    }
    else {
        $(".nav_main_content").addClass("nav_sidenav_open");
    }
    /*$(".nav_main_content").toggleClass("nav_sidenav_open");
    $("#_nav_filter_side").toggleClass("nav_sidenav_open");*/
} 

navSearchHelper.prototype.closeFilterBar = function() {
    $("#_nav_filter_side").removeClass("nav_sidenav_open");
    $(".nav_main_content").removeClass("nav_sidenav_open");
} 
navSearchHelper.prototype.openFilterBar = function() {
    $("#_nav_filter_side").addClass("nav_sidenav_open");
    $(".nav_main_content").addClass("nav_sidenav_open");
} 
registerSearchHelpers();

function registerSearchHelpers() {
    $(".nav_category_form :checkbox").change(function(event) {
        //event.preventDefault();
        new navSearchHelper().submitSearch();
    } );
    $(".nav_age_group_form :checkbox").change(function(event) {
        //event.preventDefault();
        new navSearchHelper().submitSearch();
    } );
    $(".nav_skills_form :checkbox").change(function(event) {
        //event.preventDefault();
        new navSearchHelper().submitSearch();
    } );
    $(".nav_brand_form :checkbox").change(function(event) {
        //event.preventDefault();
        new navSearchHelper().submitSearch();
    } );
    $(".nav_search_sorter").change(function(event){
        //event.preventDefault();
        new navSearchHelper().submitSearch();
    } )
    $(".nav_search_button").click(function(event) {
        event.preventDefault();
        new navSearchHelper().submitSearch();
        //event.stopPropagation();
    }) ;
    $("#_nav_filter_btn").click(function(event) {
        event.preventDefault();
        new navSearchHelper().toggleFilterBar();
        //event.stopPropagation();
    });
   /*$(".nav_main_content").click(function(event) {
        //event.preventDefault();
        new navSearchHelper().closeFilterBar();
    })*/
}


