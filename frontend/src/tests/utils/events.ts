import { act } from "@testing-library/react";

const click = async (button: HTMLElement) => {
  await act(async () => {
    button.click();
  });
};

export { click };
