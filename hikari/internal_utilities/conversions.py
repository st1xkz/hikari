#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © Nekokatt 2019-2020
#
# This file is part of Hikari.
#
# Hikari is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hikari is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Hikari. If not, see <https://www.gnu.org/licenses/>.
"""
Media tranformation utilities.
"""
import base64

from hikari.internal_utilities import type_hints


def image_bytes_to_image_data(img_bytes: bytes) -> type_hints.Nullable[str]:
    """
    Encode image bytes into an image data string.

    Args:
        img_bytes:
            The image bytes or `None`.

    Raises:
        ValueError:
            If the image type passed is not supported.

    Returns:
        The image_bytes given encoded into an image data string or `None`.

    Note:
        Supported image types: .png, .jpeg, .jfif, .gif, .webp
    """
    if img_bytes is None:
        return None

    if img_bytes[:8] == b"\211PNG\r\n\032\n":
        img_type = "image/png"
    elif img_bytes[6:10] in (b"Exif", b"JFIF"):
        img_type = "image/jpeg"
    elif img_bytes[:6] in (b"GIF87a", b"GIF89a"):
        img_type = "image/gif"
    elif img_bytes.startswith(b"RIFF") and img_bytes[8:12] == b"WEBP":
        img_type = "image/webp"
    else:
        raise ValueError("Unsupported image type passed")

    image_data = base64.b64encode(img_bytes).decode()

    return f"data:{img_type};base64,{image_data}"


def guild_id_to_shard_id(guild_id: int, shard_count: int) -> int:
    """
    Get the shard id of the given guild id.

    Args:
        guild_id:
            The ID of the guild.
        shard_count:
            The ammount of shards that are being used overal to connect to Discord.

    Returns:
        The shard the given guild is in.
    """
    return (guild_id >> 22) % shard_count