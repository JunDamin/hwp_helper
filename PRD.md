
# Product Requirements Document: HWP Helper GUI Migration to Flet

## 1. Overview

This document outlines the requirements for migrating the HWP Helper application's graphical user interface (GUI) from customtkinter to the Flet framework. The goal is to modernize the application's look and feel, improve performance, and simplify the codebase.

## 2. Background

The HWP Helper is a desktop application that provides a set of tools and templates to assist users working with Hangul Word Processor (HWP) documents. The current GUI is built with customtkinter, a Python UI library based on Tkinter. While functional, migrating to Flet offers several advantages:

*   **Modern UI/UX:** Flet provides a more modern set of widgets and a more fluid user experience.
*   **Cross-platform potential:** Flet is designed to be cross-platform, which could allow for future expansion to other operating systems.
*   **Simplified development:** Flet's declarative UI approach can lead to more concise and readable code.
*   **Web-based potential:** Flet applications can be run in a web browser, which could open up new possibilities for the HWP Helper.

## 3. Functional Requirements

The migrated application must retain all existing functionality of the HWP Helper. This includes, but is not limited to:

### 3.1. Main Window

*   The main application window should be resizable and have a title bar displaying the application name and version.
*   The window should have a "close" button that saves the current application state (e.g., the active tab) before closing.
*   The window should support "always on top" functionality.
*   The window should be able to be positioned and resized on the screen (fullscreen, half-screen).

### 3.2. Navigation

*   The application should have a main navigation area that allows users to switch between the "Features" and "Templates" sections. This will be a Tab-based navigation.
*   A navigation bar with buttons for "Show HWP", "Fullscreen", "Half Screen", and "Always on Top" should be present.

### 3.3. Features Section

*   The "Features" section should display a scrollable list of buttons for various HWP-related functions.
*   The buttons should be organized into the following categories:
    *   글자 모양 기능 (Character Shape Features)
    *   문단 정렬 기능 (Paragraph Alignment Features)
    *   테이블 관련 기능 (Table Features)
    *   페이지 관련 기능 (Page Layout Features)
    *   메모 관련 기능 (Memo Features)
    *   검토 기능 (Review Features)
*   Each button should have a descriptive name and a tooltip that explains its function.
*   The layout should be a grid with a specified number of columns.

### 3.4. Templates Section

*   The "Templates" section should display a list of available templates, organized by category.
*   Categories should be displayed in collapsible sections.
*   Each template should be represented by a button with a name and a preview image.
*   Clicking a template button should insert the corresponding template into the active HWP document.
*   The section should include an "Add Template" button that opens a form for adding a new template.
*   The "Add Template" form should allow the user to specify a category and a name for the new template.
*   The section should include an "Update Templates" button that opens a form for managing existing templates.
*   The "Update Templates" form should allow users to rename and delete templates.

### 3.5. Font Styles

*   The application should provide a way to save and apply font styles.
*   A collapsible section for "Font Styles" should be available.
*   Users should be able to save the current font style from the HWP document.
*   Saved font styles should be displayed as buttons.
*   Each font style button should show a preview of the font.
*   Buttons to apply the character, paragraph, or both styles should be provided.
*   A button to delete a saved font style should be provided.

## 4. Non-Functional Requirements

*   **UI/UX:** The application should have a clean, modern, and intuitive user interface. The UI should be responsive and provide a smooth user experience.
*   **Performance:** The application should be performant and not introduce any noticeable lag or delays.
*   **Code Quality:** The codebase should be well-structured, readable, and maintainable.
*   **Error Handling:** The application should handle errors gracefully and provide informative feedback to the user.

## 5. Component Mapping

The following table maps the existing customtkinter components to their proposed Flet equivalents.

| CustomTkinter Component | Flet Component | Notes |
| :--- | :--- | :--- |
| `ctk.CTk` | `ft.Page` | The main application window. |
| `ctk.CTkFrame` | `ft.Container` | A general-purpose container. |
| `ctk.CTkScrollableFrame` | `ft.Column` with `scroll=True` | A scrollable container. |
| `ctk.CTkButton` | `ft.ElevatedButton`, `ft.TextButton`, `ft.IconButton` | Buttons for various actions. |
| `ctk.CTkLabel` | `ft.Text` | For displaying text. |
| `ctk.CTkEntry` | `ft.TextField` | For text input. |
| `ctk.CTkTabview` | `ft.Tabs` | For tabbed navigation. |
| `ctk.CTkToplevel` | `ft.AlertDialog` or a new `ft.Page` | For dialogs and forms. |
| `ToolTip` (custom) | `ft.Tooltip` | For displaying tooltips. |
| `CollapsibleFrame` (custom) | `ft.ExpansionPanel` | For collapsible sections. |
| `GridFrame` (custom) | `ft.GridView` or `ft.Row`/`ft.Column` | For grid layouts. |
| `ImageLabel` (custom) | `ft.Image` | For displaying images. |

## 6. Development Plan

The migration will be performed in the following phases:

1.  **Setup:** Set up a new Flet project and install the necessary dependencies.
2.  **Core Structure:** Recreate the main application window, tabs, and navigation bar using Flet components.
3.  **Features Section:** Implement the "Features" section with all its buttons and functionality.
4.  **Templates Section:** Implement the "Templates" section, including the collapsible categories, template buttons, and the "Add/Update Template" forms.
5.  **Font Styles:** Implement the "Font Styles" feature.
6.  **Styling and Theming:** Apply a consistent and modern theme to the application.
7.  **Testing and Debugging:** Thoroughly test the application to ensure all functionality is working as expected and fix any bugs.
8.  **Packaging:** Package the application for distribution.

