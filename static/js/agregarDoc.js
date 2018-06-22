function _toConsumableArray(arr) { if (Array.isArray(arr)) { for (var i = 0, arr2 = Array(arr.length); i < arr.length; i++) { arr2[i] = arr[i]; } return arr2; } else { return Array.from(arr); } }

//Get all input elements of the form with a .input class
var getInputs = function getInputs(container) {
    return [].concat(_toConsumableArray(container.querySelectorAll('.input')));
};

//Get all fieldsets within the form element 

var getFieldsets = function getFieldsets(container) {
    return [].concat(_toConsumableArray(container.querySelectorAll('fieldset')));
};

//Get an Array with the distance of each fieldset element to apply a margin
var getArrayOfMargins = function getArrayOfMargins(fieldsetsContainer) {
    return getFieldsets(fieldsetsContainer).map(function (fieldset, i) {
        return fieldset.offsetHeight * i;
    });
};

// Apply or add .focus class according if a element gain or loss its focus.
var inpustEvent = function inpustEvent(container) {

    getInputs(container).map(function (input) {
        input.addEventListener("focusin", function (e) {
            var inputParent = e.target.parentElement;

            if (!inputParent.classList.contains('focus')) {
                inputParent.classList.add('focus');
            }
        });
        input.addEventListener("blur", function (e) {
            var inputParent = e.target.parentElement;
            if (input.required) {
                if (e.target.value == "") {
                    inputParent.classList.replace('focus', 'error');
                } else {
                    inputParent.classList.remove('error');
                }
            } else {
                if (e.target.value == "") {
                    inputParent.classList.remove('focus');
                }
            }
        });
        input.addEventListener('keydown', function (e) {

            if (e.key === "Enter" || e.key === "Tab") {
                e.preventDefault();
                if (e.key === "Enter") {
                    container.querySelectorAll('.next')[0].click();
                }
            }
        });
    });
};
//Add function Navegation Prev and Next fr the fieldsets elements

var formNavigation = function formNavigation(buttonsContainer, fieldsetsContainer, progressBarContainer, i) {
    
    var margins = [0, 600, 1200, 1800, 2400],
        margin = void 0,
        progressBarItems = [].concat(_toConsumableArray(progressBarContainer.querySelectorAll('li')));
    buttonsContainer.addEventListener("click", function (e) {
        console.log(margins);
        e.preventDefault();

        var el = e.target,
            getFieldsetsLenght = getFieldsets(fieldsetsContainer).length;

        if (el.tagName === "BUTTON") {
            console.log("tres");
            if (el.classList.contains("prev")) {
                if (i > 0) {
                    margin = -margins[i - 1];
                    i--;
                } else {
                    i = 0;
                }

                fieldsetsContainer.style.marginTop = margin + "px";
            } else if (el.classList.contains("next")) {
                console.log("cuatro");
                if (formValidation(i, fieldsetsContainer, progressBarContainer)) {
                    console.log(-margins[i + 1]);
                    console.log(getFieldsetsLenght);
                    if (i == getFieldsetsLenght - 1) {
                        console.log("ayuda1");
                        // margin = margins[0];
                        i = getFieldsetsLenght - 1;
                        document.querySelectorAll('.submit-button')[0].classList.add('active');
                    } else {
                        console.log("ayuda2");
                        console.log(margin);
                        margin = -margins[i + 1];
                        console.log(margin);
                        i++;
                    }
                }
                fieldsetsContainer.style.marginTop = margin + "px";
            }
        }
        progressBarItems.forEach(function (element) {
            if (progressBarItems[i] === element) {
                element.classList.add('current');
                if (element.classList.contains('complete')) {
                    element.classList.remove('current');
                }
            } else {
                element.classList.remove('current');
            }
        });
    });
    progressBar(progressBarContainer, fieldsetsContainer);
};

//Add function navegation with the progress bar. 

var progressBar = function progressBar(progressBarContainer, fieldsetsContainer) {

    var links = [].concat(_toConsumableArray(progressBarContainer.querySelectorAll('a'))),
        margins = getArrayOfMargins(fieldsetsContainer);

    progressBarContainer.addEventListener('click', function (e) {
        e.preventDefault();
        if (e.target.tagName === "A" && (e.target.parentElement.classList.contains('complete') || e.target.parentElement.classList.contains('current'))) {
            var index = links.indexOf(e.target);
            fieldsetsContainer.style.marginTop = -margins[index] + "px";
        }
    });
};
//Form Validation for each group of inputs within the fieldsets elements. Here you can add your own custom validation.

var formValidation = function formValidation(i, fieldsetsContainer, progressBarContainer) {

    var fieldsets = getFieldsets(fieldsetsContainer),
        currentFieldset = fieldsets[i],
        inputs = getInputs(currentFieldset);

    for (var key in inputs) {

        var input = inputs[key];
        if (input.required) {
            if (input.value != "") {

                input.parentElement.classList.remove('error');
                continue;
            } else {

                console.dir(input.required);
                input.parentElement.classList.add('error');
                return false;
            }
        }
    }
    progressBarContainer.querySelectorAll('li')[i].classList.add('complete');

    return true;
};

//Submit button. Here you can add ajax request.
var submit = function submit(container, fieldsetsContainer) {
    var submitButton = container.querySelectorAll("input[type='submit']");
    container.addEventListener('click', function (e) {
        if (e.target.type === "submit" && e.target.tagName === "INPUT") {
            e.preventDefault();
            var overlay = document.createElement('div');
            overlay.classList.add('overlay');
            overlay.innerHTML = ' <span class="load"></span>';
            container.appendChild(overlay);
            setTimeout(function () {
                overlay.innerHTML = ' <span class="success">\u2714 Haz agregado exitosamente un documento</span>';
            }, 2000);
        }
    });
};

var stepsforminit = function stepsforminit(container) {
    var form = container,
        fieldsetsContainer = container.querySelectorAll('#fieldset-container')[0],
        progressBarContainer = container.querySelectorAll('#progress-bar')[0],
        buttonsContainer = container.querySelectorAll('.tab-nav')[0],
        i = 0;
    inpustEvent(form);
    formNavigation(buttonsContainer, fieldsetsContainer, progressBarContainer, i);
    submit(form, fieldsetsContainer);
};

stepsforminit(document.getElementById('form-wrapper'));