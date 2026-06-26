function updateCounter(input) {
    const expectedLength = parseInt(input.dataset.length);
    const valueLength = input.value.length;

    const counter = input.parentElement.querySelector(".counter");

    if (!counter) {
        return;
    }

    counter.textContent = valueLength + "/" + expectedLength;

    input.classList.remove("field-ok");
    input.classList.remove("field-error");
    input.classList.remove("field-empty");

    counter.classList.remove("counter-ok");
    counter.classList.remove("counter-error");
    counter.classList.remove("counter-empty");

    const isRequired = input.classList.contains("required-fixed");
    const isOptional = input.classList.contains("optional-fixed");

    if (valueLength === 0 && isOptional) {
        input.classList.add("field-empty");
        counter.classList.add("counter-empty");
        return;
    }

    if (valueLength === expectedLength) {
        input.classList.add("field-ok");
        counter.classList.add("counter-ok");
        return;
    }

    if (isRequired || valueLength > 0) {
        input.classList.add("field-error");
        counter.classList.add("counter-error");
        return;
    }

    input.classList.add("field-empty");
    counter.classList.add("counter-empty");
}


function updateImsi() {
    const mcc = document.querySelector("input[name='imsi_mcc']").value;
    const mnc = document.querySelector("input[name='imsi_mnc']").value;
    const msin = document.querySelector("input[name='imsi_msin']").value;

    const imsi = mcc + mnc + msin;

    const hidden = document.querySelector("#imsi-hidden");
    const preview = document.querySelector("#imsi-preview");
    const totalCounter = document.querySelector("#imsi-total-counter");

    hidden.value = imsi;
    preview.value = imsi;

    totalCounter.textContent = imsi.length + "/15";

    preview.classList.remove("field-ok");
    preview.classList.remove("field-error");
    totalCounter.classList.remove("counter-ok");
    totalCounter.classList.remove("counter-error");

    if (imsi.length === 15) {
        preview.classList.add("field-ok");
        totalCounter.classList.add("counter-ok");
    } else {
        preview.classList.add("field-error");
        totalCounter.classList.add("counter-error");
    }
}


document.addEventListener("DOMContentLoaded", function () {
    const countedInputs = document.querySelectorAll(".counted");

    countedInputs.forEach(function (input) {
        updateCounter(input);

        input.addEventListener("input", function () {
            updateCounter(input);
            updateImsi();
        });
    });

    updateImsi();
});
