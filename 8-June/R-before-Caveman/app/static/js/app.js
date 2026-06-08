(() => {
    const updateCheckboxGroupState = (group) => {
        const minimumChecks = Number(group.dataset.minChecks || 1);
        const checkboxes = Array.from(group.querySelectorAll('input[type="checkbox"]'));
        const checkedCount = checkboxes.filter((checkbox) => checkbox.checked).length;
        const isValid = checkedCount >= minimumChecks;
        const feedback = group.querySelector(".group-feedback");

        group.classList.toggle("is-invalid", !isValid);
        if (feedback) {
            feedback.classList.toggle("d-block", !isValid);
        }
        return isValid;
    };

    const forms = document.querySelectorAll(".needs-validation");
    forms.forEach((form) => {
        form.addEventListener("submit", (event) => {
            let isValid = form.checkValidity();

            form.querySelectorAll("[data-checkbox-group]").forEach((group) => {
                if (!updateCheckboxGroupState(group)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                event.preventDefault();
                event.stopPropagation();
            }

            form.classList.add("was-validated");
        });
    });

    document.querySelectorAll("[data-checkbox-group]").forEach((group) => {
        group.querySelectorAll('input[type="checkbox"]').forEach((checkbox) => {
            checkbox.addEventListener("change", () => {
                updateCheckboxGroupState(group);
            });
        });
    });

    document.querySelectorAll("form[data-confirm]").forEach((form) => {
        form.addEventListener("submit", (event) => {
            const message = form.dataset.confirm || "Are you sure you want to continue?";
            if (!window.confirm(message)) {
                event.preventDefault();
            }
        });
    });
})();
