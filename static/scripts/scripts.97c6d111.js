angular.module("templates-main",["views/link-item.html","views/main.html"]),angular.module("views/link-item.html",[]).run(["$templateCache",function(a){"use strict";a.put("views/link-item.html",'<div class="list main active"><div class=list-tile-left><span class="icon-round orange"><i class="icon {{ link.icon }}"></i></span></div><div class=list-tile-center><h2><a ng-click="clickLink($event, link)" href="{{ link.url }}">{{ link.title }}</a></h2><h3 class=domain>{{ link.domain }}</h3></div><div class=list-tile-right><a class=link-go href="{{ link.url }}"><svg version=1.1 id=Layer_1 xmlns=http://www.w3.org/2000/svg xmlns:xlink=http://www.w3.org/1999/xlink x=0px y=0px width=16px height=16px viewbox="0 0 16 16" enable-background="new 0 0 512 512" xml:space=preserve><path transform="scale(0.03125, 0.03125)" d="M341.342,0H512v170.664l-64,64V117.336L213.336,352L160,298.658L394.658,64H277.342L341.342,0z M0,85.336h320l-64,64H64V448h298.658V256l64-64v320H0V85.336z"></svg></a></div></div><div btf-markdown=link.body class=list-body></div>')}]),angular.module("views/main.html",[]).run(["$templateCache",function(a){"use strict";a.put("views/main.html",'<header><div class=container><div class="list header"><div class=list-tile-left><span class="icon-round white-25 vertical-center" ng-click=toggleSearchBar()><i class="icon icon-search" ng-show=isPhone()></i> <i class="icon icon-chain" ng-hide=isPhone()></i></span></div><div class=list-tile-center><div class=title ng-show="isPhone() ? !searchBarVisible : true"><h1>Insightful Reads</h1><h3 class=domain>http://read.yiransheng.com</h3></div><div class=search ng-show="isPhone() ? searchBarVisible : true"><input placeholder=Search... ng-model=query ng-model-options="{ updateOn: \'blur\' }" ng-model-clear ng-enter-blur ng-change="commitSearch(query)"></div></div></div></div></header><div class="row top-row" ng-if=false><div class=col-md-8><form class="form-wrapper cf"><input ng-model=query ng-model-options="{ updateOn: \'change\' }" ng-model-clear placeholder="Search..."> <i class="icon icon-search"></i></form></div></div><div class=container><div ng-show=showSearch()><div ng-repeat="link in search_results"><ng-include src="\'views/link-item.html\'"></ng-include></div></div><div ng-show=showAll()><div ng-repeat="link in links" ng-class="{ \'active\' : !isPhone() || link.collapsed }"><ng-include src="\'views/link-item.html\'"></ng-include></div><div class=pager ng-show=has_more><a ng-click=load_next_page()>More >></a></div></div><div ng-show=error>{{ error }}</div></div>')}]);try{angular.module("templates-main")}catch(err){angular.module("templates-main",[])}angular.module("bookmarkApp",["ngAnimate","ngCookies","ngResource","ngRoute","ngSanitize","ngTouch","btford.markdown","templates-main"]).config(["$routeProvider",function(a){a.when("/",{templateUrl:"views/main.html",controller:"MainCtrl",reloadOnSearch:!0}).otherwise({redirectTo:function(a,b,c){return"/"+(c.search?"?search="+c.search:"")}})}]).constant("settings",{api:"/api/v1/",SEARCH_STATUS:{IDLE:0,SEARCHING:1,DONE:2,ERROR:3}}).run(["$rootScope","$http","$location","settings","iconMapping",function(a,b,c,d,e){a.links=[],a.has_more=!0,a.next_page=null,a.error=null,a.load_next_page=function(f){a.has_more&&b({method:"GET",url:d.api+"link",params:{next:a.next_page}}).success(function(b){b.data.forEach(function(a){a.icon=e(a.domain)}),c.search("search",null),a.links=f?b.data||[]:a.links.concat(b.data),a.has_more=b.more,a.next_page=b.next}).error(function(){a.error="Oops, something went wrong. "})}}]),angular.module("bookmarkApp").factory("iconMapping",function(){var a={"facebook.com":"icon-facebook-square","twitter.com":"icon-twitter","pinterest.com":"icon-pinterest-square","plus.google.com":"icon-google-plus-square","linkedin.com":"icon-linkedin","github.com":"icon-github-alt","youtube.com":"icon-youtube","dropbox.com":"icon-dropbox","stackoverflow.com":"icon-stack-overflow","wordpress.com":"icon-wordpress","reddit.com":"icon-reddit","news.ycombinator.com":"icon-hacker-news","default":"icon-unlink"};return function b(c){if(c=c||"",a[c])return a[c];var d=c.split(".");return 3==d.length?(c=d[1]+"."+d[2],b(c)):a.default}}),angular.module("bookmarkApp").factory("responsiveUtils",function(){var a=16,b=30*a,c=48*a,d=62*a,e=75*a;return{breakPoints:{xs:b,sm:c,md:d,lg:e},getResponsiveClass:function(){var a=window.innerWidth;return a<this.breakPoints.xs?"xxs":a<this.breakPoints.sm?"xs":a<this.breakPoints.md?"sm":a<this.breakPoints.lg?"md":"lg"}}}),angular.module("bookmarkApp").factory("Search",["$http","$q","settings","iconMapping",function(a,b,c,d){return{status:c.SEARCH_STATUS.IDLE,search:function(e){var f=this;this.status=c.SEARCH_STATUS.SEARCHING;var g=b.defer();return a({method:"GET",url:c.api+"search/link",params:{query:e}}).success(function(a){f.status=c.SEARCH_STATUS.DONE,a.data.forEach(function(a){a.icon=d(a.domain)}),g.resolve(a.data)}).error(function(a){f.status=c.SEARCH_STATUS.ERROR,g.reject(a)}),g.promise},clearSearch:function(){this.status=c.SEARCH_STATUS.IDLE},isLoading:function(){return this.status==c.SEARCH_STATUS.SEARCHING}}}]),angular.module("bookmarkApp").controller("MainCtrl",["$scope","$rootScope","$http","$routeParams","$location","$window","settings","Search","iconMapping","responsiveUtils",function(a,b,c,d,e,f,g,h,i,j){a.search_results=[],a.Search=h,a.query=d.search||"",a.showAll=function(){return!b.error&&h.status===g.SEARCH_STATUS.IDLE},a.showSearch=function(){return!b.error&&h.status===g.SEARCH_STATUS.DONE},a.toggleSearchBar=function(){var b=j.getResponsiveClass();return"lg"===b||"md"===b?!0:void(a.searchBarVisible=!a.searchBarVisible)},a.commitSearch=function(a){a&&0!==a.length?e.search("search",a.toLowerCase()):e.search("search",null)},d.next&&!a.query?(b.next_page=d.next,b.load_next_page(!0)):a.query?(b.error=0/0,h.search(a.query).then(function(b){a.search_results=b},function(){b.error='Error Searching: "'+query+'"'})):(h.clearSearch(),b.load_next_page()),a.clickLink=function(a,b){var c=j.getResponsiveClass();"lg"!==c&&"md"!==c&&(a.preventDefault(),a.stopPropagation(),b.collapsed=!b.collapsed)},a.isPhone=function(){var a=j.getResponsiveClass();return"lg"===a||"md"===a?!1:!0},window.onresize=function(){b.$digest()}}]),angular.module("bookmarkApp").directive("ngModelClear",["$rootScope",function(a){return{restrict:"A",require:["ngModel","ngModelOptions"],link:function(b,c,d,e){var f=e[0];c.bind("keyup",function(){f.$isEmpty(c.val())&&(f.$setViewValue(""),f.$commitViewValue(),c[0].blur(),a.$digest())})}}}]).directive("ngEnterBlur",function(){return{restrict:"A",require:["ngModel","ngModelOptions"],link:function(a,b,c,d){d[0];b.bind("keyup",function(a){13===a.which&&a.target.blur()})}}});