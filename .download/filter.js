$(document).ready(function() {
  oldVisible = 'Bund';

  window.addEventListener("hashchange", updateVisible, false);

  function updateVisible() {
    // rawHash ist z.B. "#Bund"
    rawHash = $(location).attr('hash').replace(/^#/, "");

    // Wir wollen die Umlaute nicht codiert haben
    decodedHash = decodeURIComponent(rawHash);

    // Aktiven Link hervorheben
    activeMenuItem = 'header a:contains(' + decodedHash + ')';

    // Bei aktivem Button hervorhebung entfernen
    oldVisibleMenuItem = 'header a:contains(' + oldVisible + ')';
    if ($(oldVisibleMenuItem).hasClass('activeMenuItem')) {
      $(oldVisibleMenuItem).removeClass('activeMenuItem');
    }

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
});
