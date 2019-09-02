import { TestBed } from '@angular/core/testing';

import { ReaderViewService } from './reader-view.service';

describe('ReaderViewService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: ReaderViewService = TestBed.get(ReaderViewService);
    expect(service).toBeTruthy();
  });
});
