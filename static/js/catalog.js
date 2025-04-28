document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.product.admin .details h3, .product.admin .details .price')
      .forEach(elem => {
        elem.style.cursor = 'pointer';
        elem.addEventListener('click', () => {
          const card = elem.closest('.product');
          const id = card.dataset.id;
          const name = card.querySelector('h3').innerText;
          const url = card.querySelector('img').src;
          const price = card.querySelector('.price').innerText.replace('$', '');
  
          const newName = prompt('New name:', name);
          const newUrl = prompt('New image URL:', url);
          const newPrice = prompt('New price:', price);
  
          if (newName && newUrl && newPrice) {
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '/goods/update';
            [['id', id], ['name', newName], ['url', newUrl], ['price', newPrice]]
              .forEach(([k, v]) => {
                const i = document.createElement('input');
                i.type  = 'hidden';
                i.name  = k;
                i.value = v;
                form.appendChild(i);
              });
            document.body.appendChild(form);
            form.submit();
          }
        });
      });
  
    document.querySelectorAll('.product.user').forEach(card => {
      const counterEl = card.querySelector('.counter');
      const minusBtn = card.querySelector('.minus');
      const plusBtn = card.querySelector('.plus');
      const formAdd = card.querySelector('.form-add');
      const formRem = card.querySelector('.form-remove');
  
      let count = parseInt(counterEl.dataset.count || counterEl.innerText, 10);
      if (isNaN(count)) count = 0;
  
      function update() {
        counterEl.innerText = count;
        minusBtn.disabled = (count <= 0);
      }
  
      update();
  
      minusBtn.addEventListener('click', () => {
        if (count > 0) {
          count--;
          update();
          formRem.submit();
        }
      });
  
      plusBtn.addEventListener('click', () => {
        count++;
        update();
        formAdd.submit();
      });
    });
  });
  