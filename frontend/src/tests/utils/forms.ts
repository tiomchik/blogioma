import { screen } from "@testing-library/react";
import { click } from "./events";
import userEvent from "@testing-library/user-event";
import { expect } from "vitest";

const clickSubmitButton = async () => {
  const submitButton = screen.getByRole("button");
  await click(submitButton);
};

const pasteIntoFieldByLabelText = (labelText: string, value: string) => {
  const field = getFirstElementByLabelText(labelText);
  focusAndPaste(field, value);
};

const getFirstElementByLabelText = (labelText: string): HTMLInputElement => {
  return screen.getAllByLabelText(labelText, {
    exact: false,
  })[0] as HTMLInputElement;
};

const focusAndPaste = (inputElement: HTMLInputElement, text: string) => {
  inputElement.focus();
  userEvent.paste(text);
};

const uploadDummyPfp = async (
  fileName: string = "pfp.png",
  fileType: string = "image/png"
): Promise<void> => {
  const pfpField = getFirstElementByLabelText("Profile picture");
  const file = createDummyFile(fileName, fileType);
  await userEvent.upload(pfpField, file);
};

const createDummyFile = (fileName: string, fileType: string): File => {
  return new File([], fileName, { type: fileType });
};

const expectErrorMessage = (message: RegExp | string) => {
  const error = screen.getByText(message);
  expect(error).toBeDefined();
};

const expectNoErrorMessage = (message: RegExp | string) => {
  const error = screen.queryByText(message);
  expect(error).toBeNull();
};

export {
  clickSubmitButton,
  pasteIntoFieldByLabelText,
  uploadDummyPfp,
  createDummyFile,
  expectErrorMessage,
  expectNoErrorMessage
};
