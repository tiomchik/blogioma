import {
  expectErrorMessage,
  expectNoErrorMessage,
  pasteIntoFieldByLabelText,
  renderInputWithFormProvider,
} from "@/tests/utils";
import { beforeEach, describe, test } from "vitest";
import UsernameInput, { USERNAME_FIELD_LABEL } from "./";
import userEvent from "@testing-library/user-event";

const BLANK_USERNAME_ERROR_MESSAGE = /Username cannot be blank/;

describe("without optional prop", () => {
  beforeEach(() => {
    renderInputWithFormProvider(<UsernameInput />);
  });

  test("displays error of blank username", async () => {
    pasteIntoFieldByLabelText(USERNAME_FIELD_LABEL, "");
    await userEvent.tab();
    expectErrorMessage(BLANK_USERNAME_ERROR_MESSAGE);
  });

  test("displays error of too short username", async () => {
    pasteIntoFieldByLabelText(USERNAME_FIELD_LABEL, "a");
    await userEvent.tab();
    expectErrorMessage(/Username should be more than \d+ characters long/);
  });

  test("displays error of too long username", async () => {
    pasteIntoFieldByLabelText(USERNAME_FIELD_LABEL, "a".repeat(100));
    await userEvent.tab();
    expectErrorMessage(/Username should be less than \d+ characters long/);
  });
});

test("doesn't display error of blank field if optional = true", async () => {
  renderInputWithFormProvider(<UsernameInput optional={true} />);
  pasteIntoFieldByLabelText(USERNAME_FIELD_LABEL, "");
  await userEvent.tab();
  expectNoErrorMessage(BLANK_USERNAME_ERROR_MESSAGE);
});
