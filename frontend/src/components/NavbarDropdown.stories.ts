import type { Meta, StoryObj } from '@storybook/svelte';
import NavbarDropdown from "./NavbarDropdown.svelte";

const meta = {
  title: 'Component/NavbarDropdown',
  component: NavbarDropdown,
  tags: ['autodocs'],
} satisfies Meta<NavbarDropdown>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {};
