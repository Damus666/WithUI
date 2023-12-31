import pygame

from ._constants import _SCROLLBAR_SIZE
from . import _base as _wuib


class _VScrollbar(_wuib._Element):
    def _on_init(self):
        self.set(can_press=False, can_hover=False, has_dark_bg=True, width=_SCROLLBAR_SIZE,
                 min_width=_SCROLLBAR_SIZE, max_width=_SCROLLBAR_SIZE, ignore_scroll=True, draw_top=True)
        self.__enter__()
        self.handle: _wuib._Element = _wuib._Element()
        self._children.append(self.handle)
        self.handle.set(width=_SCROLLBAR_SIZE, min_width=_SCROLLBAR_SIZE,
                        max_width=_SCROLLBAR_SIZE, ignore_scroll=True)
        self.handle_pos = 0
        self.__exit__()

    def _update(self):
        if not self._parent.settings.can_scroll_v or self._parent.settings.height >= self._parent._tot_h:
            self.settings.active = self.settings.visible= False
            return
        self.settings.active = self.settings.visible = True
        self.settings.height = self.settings.max_height = self.settings.min_height = self._parent.settings.height
        self.settings.free_position = pygame.Vector2(
            self._parent.settings.width-self.settings.width, 0)

        self._pre_update()

        self.handle_size = (self.settings.height *
                            self._parent.settings.height)/(self._parent._tot_h+0.001)
        scroll_v = (self.handle_pos*self._parent._tot_h) / \
            (self.settings.height+0.001)
        self.handle.settings.free_position = pygame.Vector2(0, self.handle_pos)
        self.handle.settings.height = self.handle.settings.min_height = self.handle.settings.max_height = self.handle_size
        self._parent.settings.scroll_offset.y = scroll_v

        self._post_update()

        if self.handle.status.pressing:
            prev = self.handle_pos
            self.handle_pos += _wuib._UIManager.mouse_rel[1]
            if self.handle_pos < 0:
                self.handle_pos = 0
            if self.handle_pos > self.settings.height-self.handle_size:
                self.handle_pos = self.settings.height-self.handle_size
            self.handle.settings.free_position = pygame.Vector2(
                0, self.handle_pos)
            if prev != self.handle_pos: self.handle._set_dirty()
        else:
            if self.status._hovering or self.handle.status.hovering or self._parent.status._hovering:
                for event in _wuib._UIManager.frame_events:
                    if event.type == pygame.MOUSEWHEEL:
                        self.handle_pos += (-event.y*self.settings.height)/100
                        if self.handle_pos < 0:
                            self.handle_pos = 0
                        if self.handle_pos > self.settings.height-self.handle_size:
                            self.handle_pos = self.settings.height-self.handle_size
                        self.handle.settings.free_position = pygame.Vector2(
                            0, self.handle_pos)
                        self.handle._set_dirty()


class _HScrollbar(_wuib._Element):
    def _on_init(self):
        self.set(can_press=False, can_hover=False, has_dark_bg=True, height=_SCROLLBAR_SIZE,
                 min_height=_SCROLLBAR_SIZE, max_height=_SCROLLBAR_SIZE, ignore_scroll=True, draw_top=True)
        self.__enter__()
        self.handle = _wuib._Element()
        self._children.append(self.handle)
        self.handle.set(height=_SCROLLBAR_SIZE, min_height=_SCROLLBAR_SIZE,
                        max_height=_SCROLLBAR_SIZE, ignore_scroll=True)
        self.handle_pos = 0
        self.__exit__()

    def _update(self):
        if not self._parent.settings.can_scroll_h or self._parent.settings.width >= self._parent._tot_w:
            self.settings.active = self.settings.visible= False
            return
        self.settings.active = self.settings.visible = True
        self.settings.width = self.settings.max_width = self.settings.min_width = self._parent.settings.width
        self.settings.free_position = pygame.Vector2(
            0, self._parent.settings.height-self.settings.height)

        self._pre_update()

        self.handle_size = (self.settings.width *
                            self._parent.settings.width)/(self._parent._tot_w+0.001)
        scroll_v = (self.handle_pos*self._parent._tot_w) / \
            (self.settings.width+0.001)
        self.handle.settings.free_position = pygame.Vector2(self.handle_pos, 0)
        self.handle.settings.width = self.handle.settings.min_width = self.handle.settings.max_width = self.handle_size
        self._parent.settings.scroll_offset.x = scroll_v

        self._post_update()

        if self.handle.status.pressing:
            prev = self.handle_pos
            self.handle_pos += _wuib._UIManager.mouse_rel[0]
            if self.handle_pos < 0:
                self.handle_pos = 0
            if self.handle_pos > self.settings.width-self.handle_size:
                self.handle_pos = self.settings.width-self.handle_size
            self.handle.settings.free_position = pygame.Vector2(
                self.handle_pos, 0)
            if prev != self.handle_pos: self.handle._set_dirty()
        elif not self._parent.settings.can_scroll_v or self._parent.settings.height >= self._parent._tot_h:
            if self.status._hovering or self.handle.status.hovering or self._parent.status._hovering:
                for event in _wuib._UIManager.frame_events:
                    if event.type == pygame.MOUSEWHEEL:
                        self.handle_pos += (-event.y*self.settings.width)/100
                        if self.handle_pos < 0:
                            self.handle_pos = 0
                        if self.handle_pos > self.settings.width-self.handle_size:
                            self.handle_pos = self.settings.width-self.handle_size
                        self.handle.settings.free_position = pygame.Vector2(
                            self.handle_pos, 0)
                        self.handle._set_dirty()
