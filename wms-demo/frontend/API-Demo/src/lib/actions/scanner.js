export function scanner(node, options = {}) {
  let currentOptions = options;
  let buffer = "";
  let lastTime = 0;
  const threshold = options.threshold || 50;
  const minLength = options.minLength || 3;

  function isTextInput(element) {
    return element instanceof HTMLInputElement || element instanceof HTMLTextAreaElement;
  }

  function handleKeydown(event) {
    if (event.key === "Shift" || event.key === "Alt" || event.key === "Control") {
      return;
    }

    const now = Date.now();
    if (now - lastTime > threshold) {
      buffer = "";
    }
    lastTime = now;

    if (event.key === "Enter") {
      if (buffer.length >= minLength) {
        const active = document.activeElement;
        const target = isTextInput(active) ? active : currentOptions.target;

        if (isTextInput(target)) {
          target.value = buffer;
          target.dispatchEvent(new Event("input", { bubbles: true }));
          target.dispatchEvent(new Event("change", { bubbles: true }));
          target.focus();
        }

        if (typeof currentOptions.onScan === "function") {
          currentOptions.onScan(buffer);
        }

        if (typeof currentOptions.submit === "function") {
          currentOptions.submit();
        }
      }
      buffer = "";
      return;
    }

    if (event.key.length === 1) {
      buffer += event.key;
    }
  }

  window.addEventListener("keydown", handleKeydown);

  return {
    update(newOptions) {
      currentOptions = newOptions || {};
    },
    destroy() {
      window.removeEventListener("keydown", handleKeydown);
    },
  };
}
