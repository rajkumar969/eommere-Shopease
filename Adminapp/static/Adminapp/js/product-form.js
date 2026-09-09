document.addEventListener("DOMContentLoaded", function () {

    const productName = document.getElementById("product_name");
    const slug = document.getElementById("slug");

    const imageInput = document.getElementById("image");
    const imagePreview = document.getElementById("imagePreview");


    // ==========================================
    // AUTO SLUG
    // ==========================================

    productName.addEventListener("input", function () {

        if (slug.dataset.manual === "true") {
            return;
        }

        slug.value = productName.value
            .toLowerCase()
            .trim()
            .replace(/[^a-z0-9\s-]/g, "")
            .replace(/\s+/g, "-")
            .replace(/-+/g, "-");

    });


    slug.addEventListener("input", function () {

        slug.dataset.manual = "true";

    });


    // ==========================================
    // IMAGE PREVIEW
    // ==========================================

    imageInput.addEventListener("change", function () {

        imagePreview.innerHTML = "";

        const file = this.files[0];

        if (!file) {
            return;
        }

        if (!file.type.startsWith("image/")) {

            alert("Please select a valid image.");

            this.value = "";

            return;
        }

        const reader = new FileReader();

        reader.onload = function (event) {

            const img = document.createElement("img");

            img.src = event.target.result;

            imagePreview.appendChild(img);

        };

        reader.readAsDataURL(file);

    });

});