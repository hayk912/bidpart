/* Use this script if you need to support IE 7 and IE 6. */

window.onload = function() {
	function addIcon(el, entity) {
		var html = el.innerHTML;
		el.innerHTML = '<span style="font-family: \'icons\'">' + entity + '</span>' + html;
	}
	var icons = {
			'icon-arrow-left' : '&#xe004;',
			'icon-arrow-down' : '&#xe000;',
			'icon-arrow-up' : '&#xe001;',
			'icon-arrow-right' : '&#xe002;',
			'icon-star' : '&#xe003;',
			'icon-bolt' : '&#xe005;',
			'icon-house' : '&#xe006;',
			'icon-cog' : '&#xe007;',
			'icon-mobile' : '&#xe008;',
			'icon-newspaper' : '&#xe00a;',
			'icon-cross' : '&#xe009;',
			'icon-list' : '&#xe00b;',
			'icon-archive' : '&#xe00c;',
			'icon-suitcase' : '&#xe00d;',
			'icon-gauge' : '&#xe00f;',
			'icon-user' : '&#xe00e;',
			'icon-arrow-right-2' : '&#xe010;',
			'icon-arrow-left-2' : '&#xe013;',
			'icon-arrow-left-3' : '&#xe014;',
			'icon-arrow-right-3' : '&#xe015;',
			'icon-thumbs-down' : '&#xe011;',
			'icon-compass' : '&#xe012;',
			'icon-lock' : '&#xe016;'
		},
		els = document.getElementsByTagName('*'),
		i, attr, html, c, el;
	for (i = 0; i < els.length; i += 1) {
		el = els[i];
		attr = el.getAttribute('data-icon');
		if (attr) {
			addIcon(el, attr);
		}
		c = el.className;
		c = c.match(/icon-[^\s'"]+/);
		if (c && icons[c[0]]) {
			addIcon(el, icons[c[0]]);
		}
	}
};