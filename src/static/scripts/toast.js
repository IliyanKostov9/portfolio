(function () {
  const toastOptions = { delay: 2000 };

  htmx.onLoad(() => {
    htmx.findAll(".toast").forEach((element) => {
      let toast = mdb.Toast.getInstance(element);

      if (toast && !toast.isShown()) {
        toast.dispose();
        element.remove();
      }

      if (!toast) {
        const toast = new mdb.Toast(element, toastOptions);
        toast.show();
      }
    });
  });
})();
