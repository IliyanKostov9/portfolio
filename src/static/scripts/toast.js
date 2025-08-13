(function () {
  htmx.onLoad(() => {
    htmx.findAll(".toast").forEach((element) => {
      let toast = mdb.Toast.getInstance(element);

      if (toast && !toast.isShown()) {
        toast.dispose();
        element.remove();
      }

      if (!toast) {
        const toast = new mdb.Toast(element, { autohide: true, delay: 7000 });
        toast.show();
      }
    });
  });
})();
