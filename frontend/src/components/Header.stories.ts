import type { Meta, StoryObj } from '@storybook/svelte';
import Header from "./Header.svelte";

const meta = {
  title: 'Component/Header',
  component: Header,
  tags: ['autodocs'],
} satisfies Meta<Header>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {};
