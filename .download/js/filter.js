function redirectOrUpdateVisible() {
  // rawHash ist z.B. "Bund"
  rawHash = $(location).attr('hash').replace(/^#/, "");

  if (!rawHash) {
    location.href = '#Bund';
    oldVisible = 'Bund';
  } else {
    if (typeof oldVisible == 'undefined') {
      oldVisible = 'Bund';
    }

    // Wir wollen die Umlaute nicht codiert haben
    decodedHash = decodeURIComponent(rawHash);

    // Bei aktivem Button hervorhebung entfernen
    oldVisibleMenuItem = '.navbar-start a:contains(' + oldVisible + ')';
    if ($(oldVisibleMenuItem).hasClass('activeMenuItem')) {
      $(oldVisibleMenuItem).removeClass('activeMenuItem');
    }

    // Aktiven Link hervorheben
    activeMenuItem = '.navbar-start a:contains(' + decodedHash + ')';

    // Neuen aktiven Button hervorheben
    $(activeMenuItem).addClass('activeMenuItem');

    // Alte Datensätze ausblenden
    oldVisibleItemList = '#' + oldVisible;
    if ($(oldVisibleItemList).hasClass('show')) {
      $(oldVisibleItemList).removeClass('show');
    }

    // Neue Datensätze einblenden
    activeItemList = '#' + decodedHash;
    $(activeItemList).addClass('show');

    // Aktiven Status speichern
    oldVisible = decodedHash;
  }
}
