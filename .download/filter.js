function redirectOrUpdateVisible() {
  // rawHash ist z.B. "#Bund"
  rawHash = $(location).attr('hash').replace(/^#/, "");

  if (!rawHash) {
    var url = location.href;
    location.href = '#Bund';
    oldVisible = 'Bund';
  } else {
    if (typeof oldVisible == 'undefined') {
      oldVisible = 'Bund';
    }

    // Wir wollen die Umlaute nicht codiert haben
    decodedHash = decodeURIComponent(rawHash);

    // Bei aktivem Button hervorhebung entfernen
    oldVisibleMenuItem = 'header a:contains(' + oldVisible + ')';
    if ($(oldVisibleMenuItem).hasClass('activeMenuItem')) {
      $(oldVisibleMenuItem).removeClass('activeMenuItem');
    }

    // Aktiven Link hervorheben
    activeMenuItem = 'header a:contains(' + decodedHash + ')';

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
