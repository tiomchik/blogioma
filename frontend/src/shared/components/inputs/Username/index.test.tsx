import {
  expectErrorMessage,
  pasteIntoFieldByLabelText,
  renderInputWithFormProvider,
} from "@/tests/utils";
import { beforeEach, test } from "vitest";
import UsernameInput, { USERNAME_FIELD_LABEL } from "./";
import userEvent from "@testing-library/user-event";

beforeEach(() => {
  renderInputWithFormProvider(<UsernameInput />);
});

test("displays error of blank username", async () => {
  pasteIntoFieldByLabelText(USERNAME_FIELD_LABEL, "");
  await userEvent.tab();
  expectErrorMessage(/Username cannot be blank/);
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
