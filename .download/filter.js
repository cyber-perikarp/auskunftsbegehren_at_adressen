// params.get

$(document).ready(function() {
  let params = new URLSearchParams(window.location.search)

  if (!params.has('filter')) {
    window.location.href = '/?filter=Bund';
  }
});
