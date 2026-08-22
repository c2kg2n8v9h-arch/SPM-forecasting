const { test, expect } = require('@playwright/test');

const rows = {
  all: 4,
  green: 2,
  yellow: 1,
  red: 1,
};

test.describe('operations dashboard', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle('SPM | Operations Control');
  });

  test('renders the operational overview and KPI summary', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'Good morning, Alex' })).toBeVisible();
    await expect(page.getByRole('article').filter({ hasText: 'Aircraft monitored' })).toContainText('24');
    await expect(page.getByRole('heading', { name: 'Fleet readiness' })).toBeVisible();
    await expect(page.getByRole('heading', { name: 'Needs attention' })).toBeVisible();
    await expect(page.getByRole('heading', { name: 'Arrival readiness' })).toBeVisible();
  });

  for (const view of ['Overview', 'Staging board', 'Demand forecast', 'Procurement']) {
    test(`navigates to ${view}`, async ({ page }) => {
      await page.getByRole('button', { name: view, exact: false }).first().click();
      await expect(page.locator('#page-title')).toHaveText(view);
    });
  }

  for (const status of ['green', 'yellow', 'red']) {
    test(`filters arrivals by ${status} status`, async ({ page }) => {
      await page.locator('#status-filter').selectOption(status);
      await expect(page.locator('#row-count')).toHaveText(String(rows[status]));
      await expect(page.locator('#arrival-rows tr')).toHaveCount(rows[status]);
      await expect(page.locator(`#arrival-rows .status-${status}`)).toHaveCount(rows[status]);
    });
  }

  test('restores all rows after clearing the status filter', async ({ page }) => {
    await page.locator('#status-filter').selectOption('red');
    await page.locator('#status-filter').selectOption('all');
    await expect(page.locator('#row-count')).toHaveText(String(rows.all));
  });

  for (const query of [
    ['N200SP', 1],
    ['JFK-H2', 1],
    ['VALVE-200', 1],
    ['not-found', 0],
    ['', 4],
  ]) {
    test(`searches arrivals with query ${query[0] || 'empty'}`, async ({ page }) => {
      await page.locator('#search-input').fill(query[0]);
      await expect(page.locator('#row-count')).toHaveText(String(query[1]));
    });
  }

  for (const combination of [
    ['N200SP', 'red', 1],
    ['JFK-H2', 'green', 0],
    ['VALVE-200', 'green', 0],
    ['FILTER-318', 'yellow', 1],
    ['station', 'all', 0],
  ]) {
    test(`combines search ${combination[0]} with ${combination[1]} filter`, async ({ page }) => {
      await page.locator('#search-input').fill(combination[0]);
      await page.locator('#status-filter').selectOption(combination[1]);
      await expect(page.locator('#row-count')).toHaveText(String(combination[2]));
    });
  }

  for (const [buttonName, message] of [
    ['Refresh mock data', 'Mock data refreshed locally'],
    ['Export briefing', 'Briefing prepared locally; no file was uploaded'],
  ]) {
    test(`${buttonName} stays local`, async ({ page }) => {
      const requests = [];
      page.on('request', (request) => requests.push(request.url()));
      await page.getByRole('button', { name: buttonName }).click();
      await expect(page.locator('#toast')).toHaveText(message);
      expect(requests.filter((url) => !url.startsWith('http://127.0.0.1:8080'))).toEqual([]);
    });
  }

  test('shows local mock mode and no live system connection', async ({ page }) => {
    await expect(page.locator('.mock-lock')).toHaveCount(1);
    await expect(page.getByText('No live systems connected')).toBeVisible();
  });

  test('shows all monthly mock flights and filters the schedule', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'August flight schedule' })).toBeVisible();
    await expect(page.locator('#monthly-flight-rows tr')).toHaveCount(12);
    await page.locator('#monthly-search').fill('N200SP');
    await expect(page.locator('#monthly-row-count')).toHaveText('3');
    await expect(page.locator('#monthly-flight-rows tr')).toHaveCount(3);
  });
});

test.describe('responsive dashboard', () => {
  test('keeps the main controls usable on mobile', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { name: 'Good morning, Alex' })).toBeVisible();
    await expect(page.locator('#search-input')).toBeVisible();
    await expect(page.locator('#status-filter')).toBeVisible();
    await expect(page.locator('body')).toHaveCSS('overflow-x', 'visible');
  });
});