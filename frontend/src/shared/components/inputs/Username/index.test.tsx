import {
  expectErrorMessage,
  expectNoErrorMessage,
  pasteIntoFieldByLabelText,
  renderInputWithFormProvider,
} from "@/tests/utils";
import { beforeEach, describe, test } from "vitest";
import UsernameInput, { USERNAME_FIELD_LABEL } from "./";
import userEvent from "@testing-library/user-event";
import { ERROR_BLANK, ERROR_TOO_SHORT, ERROR_TOO_LONG } from "./errorMessages";

describe("without optional prop", () => {
  beforeEach(() => {
    renderInputWithFormProvider(<UsernameInput />);
  });

  test("displays error of blank username", async () => {
    pasteIntoFieldByLabelText(USERNAME_FIELD_LABEL, "");
    await userEvent.tab();
    expectErrorMessage(ERROR_BLANK);
  });

  test("displays error of too short username", async () => {
    pasteIntoFieldByLabelText(USERNAME_FIELD_LABEL, "a");
    await userEvent.tab();
    expectErrorMessage(ERROR_TOO_LONG);
  });

  test("displays error of too long username", async () => {
    pasteIntoFieldByLabelText(USERNAME_FIELD_LABEL, "a".repeat(100));
    await userEvent.tab();
    expectErrorMessage(ERROR_TOO_SHORT);
  });
});

test("doesn't display error of blank field if optional = true", async () => {
  renderInputWithFormProvider(<UsernameInput optional={true} />);
  pasteIntoFieldByLabelText(USERNAME_FIELD_LABEL, "");
  await userEvent.tab();
  expectNoErrorMessage(ERROR_BLANK);
});
