$(document).ready(function() {
  let params = new URLSearchParams(window.location.search)

  // Wenn es keinen Filterparameter gibt, leiten wir auf "Bund" weiter
  if (!params.has('filter')) {
    window.location.href = '?filter=Bund';
  }

  // Holt den Wert des Filters
  var filter = params.get('filter');

  // Aktiven Link hervorheben
  buttonGetter = 'header a:contains(' + filter + ')';
  $(buttonGetter).addClass('activeMenuItem');

  // Das was wir sehen wollen einblenden
  activeItemGetter = '#' + filter;
  $(activeItemGetter).addClass('show');
});
