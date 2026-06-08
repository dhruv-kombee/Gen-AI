document.addEventListener("DOMContentLoaded", () => {
    const forms = document.querySelectorAll(".needs-validation");

    forms.forEach((form) => {
        form.addEventListener("submit", (event) => {
            let checkboxGroupValid = true;
            const checkboxGroupName = form.dataset.checkboxGroup;

            if (checkboxGroupName) {
                const checkboxes = form.querySelectorAll(`input[name="${checkboxGroupName}"]`);
                const errorTarget = form.querySelector("[data-checkbox-error]");
                checkboxGroupValid = Array.from(checkboxes).some((checkbox) => checkbox.checked);

                if (errorTarget) {
                    errorTarget.classList.toggle("d-none", checkboxGroupValid);
                }
            }

            if (!form.checkValidity() || !checkboxGroupValid) {
                event.preventDefault();
                event.stopPropagation();
            }

            form.classList.add("was-validated");
        });
    });

    document.querySelectorAll("[data-confirm]").forEach((element) => {
        element.addEventListener("click", (event) => {
            const message = element.getAttribute("data-confirm");
            if (!window.confirm(message)) {
                event.preventDefault();
            }
        });
    });
});

